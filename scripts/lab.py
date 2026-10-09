#!/usr/bin/env python3
"""Laboratório descartável com dois clusters Kind. Apenas biblioteca padrão."""
import argparse, base64, json, os, pathlib, shutil, ssl, subprocess, sys, time, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parents[1]
STATE = ROOT / '.state'
EVIDENCE = ROOT / 'evidence'
A, B = 'sbd-app', 'sbd-bao'
NODE_IMAGE = 'kindest/node:v1.31.4'
BAO_IMAGE = os.environ.get('POC_BAO_IMAGE', 'quay.io/openbao/openbao:2.7.1')
CALICO = 'https://raw.githubusercontent.com/projectcalico/calico/v3.29.3/manifests/calico.yaml'

def run(args, data=None, capture=True):
    p = subprocess.run(args, input=data, text=True, capture_output=capture, check=False)
    if p.returncode:
        # Evita exibir stdin, onde há material sensível.
        raise RuntimeError('Falha em '+args[0]+': '+(p.stderr or '')[:1500])
    return p.stdout or ''

def k(cluster, *args, data=None):
    return run(['kubectl', '--context', 'kind-'+cluster, *args], data)

def obj(kind, name, spec=None, namespace='poc', **extra):
    versions={'Deployment':'apps/v1','Job':'batch/v1','NetworkPolicy':'networking.k8s.io/v1',
              'ClusterRole':'rbac.authorization.k8s.io/v1','ClusterRoleBinding':'rbac.authorization.k8s.io/v1'}
    result={'apiVersion':versions.get(kind,'v1'),'kind':kind,'metadata':{'name':name}}
    if namespace: result['metadata']['namespace']=namespace
    if spec is not None: result['spec']=spec
    result.update(extra)
    return result

def apply(cluster, objects, filename):
    value={'apiVersion':'v1','kind':'List','items':objects}
    text=json.dumps(value, indent=2)
    (STATE/filename).write_text(text)
    os.chmod(STATE/filename,0o600)
    k(cluster,'apply','-f','-',data=text)

def secure_write(path, value):
    fd=os.open(path, os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
    with os.fdopen(fd,'w') as f: f.write(value)

def api(path, data=None, token=None):
    ctx=ssl.create_default_context(cafile=str(STATE/'ca.crt'))
    headers={'Content-Type':'application/json'}
    if token: headers['X-Vault-Token']=token
    req=urllib.request.Request('https://localhost:18200/v1/'+path,
        data=json.dumps(data).encode() if data is not None else None,headers=headers)
    with urllib.request.urlopen(req,context=ctx,timeout=15) as r:
        raw=r.read()
        return json.loads(raw) if raw else {}

def forward():
    p=subprocess.Popen(['kubectl','--context','kind-'+B,'-n','poc','port-forward',
        'service/openbao','18200:8200','--address','127.0.0.1'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    for _ in range(50):
        if p.poll() is not None: raise RuntimeError('Port-forward indisponível; porta 18200 em uso?')
        try:
            api('sys/seal-status'); return p
        except (OSError,urllib.error.URLError): time.sleep(.2)
    p.terminate(); raise RuntimeError('OpenBao não respondeu em 10 segundos')

def preflight():
    for cmd in ('docker','kind','kubectl','openssl'):
        if not shutil.which(cmd): raise RuntimeError('Instale '+cmd+' antes de continuar')
    run(['docker','info'])

def setup():
    preflight()
    existing=run(['kind','get','clusters']).split()
    if A in existing or B in existing:
        raise RuntimeError('Nomes do laboratório já existem. Use cleanup somente se criados por esta POC.')
    STATE.mkdir(mode=0o700,exist_ok=True); os.chmod(STATE,0o700)
    for cluster,cidr in ((A,'192.168.0.0/17'),(B,'192.168.128.0/17')):
        # CIDRs diferentes não tornam os Pods diretamente roteáveis entre clusters.
        config=f'''kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  disableDefaultCNI: true
  podSubnet: {cidr}
nodes:
- role: control-plane
'''
        path=STATE/(cluster+'.yaml'); path.write_text(config)
        run(['kind','create','cluster','--name',cluster,'--image',NODE_IMAGE,'--config',str(path)],capture=False)
        secure_write(STATE/(cluster+'.owned'),'created by this POC\n')
        # Copia fixada do manifesto; ajustar pool Calico para cada cluster.
        with urllib.request.urlopen(CALICO,timeout=60) as r: calico=r.read().decode()
        calico=calico.replace('192.168.0.0/16',cidr)
        k(cluster,'apply','-f','-',data=calico)
        k(cluster,'-n','kube-system','set','env','daemonset/calico-node','CALICO_IPV4POOL_CIDR='+cidr)
        k(cluster,'wait','--for=condition=Ready','nodes','--all','--timeout=300s')
        k(cluster,'-n','kube-system','rollout','status','daemonset/calico-node','--timeout=300s')
        ns=obj('Namespace','poc',namespace=None)
        ns['metadata']['labels']={'pod-security.kubernetes.io/enforce':'restricted','pod-security.kubernetes.io/enforce-version':'v1.31'}
        apply(cluster,[ns,obj('ServiceAccount','reader',automountServiceAccountToken=False),
                       obj('ServiceAccount','outsider',automountServiceAccountToken=False)],cluster+'-base.json')
    def nodeip(cluster):
        info=json.loads(run(['docker','inspect',cluster+'-control-plane']))[0]
        return info['NetworkSettings']['Networks']['kind']['IPAddress']
    ai,bi=nodeip(A),nodeip(B)
    secure_write(STATE/'network.json',json.dumps({'a':ai,'b':bi}))
    run(['openssl','req','-x509','-newkey','rsa:3072','-nodes','-days','7','-subj','/CN=POC-CA',
         '-keyout',str(STATE/'ca.key'),'-out',str(STATE/'ca.crt')])
    run(['openssl','req','-newkey','rsa:3072','-nodes','-subj','/CN=openbao.poc',
         '-keyout',str(STATE/'server.key'),'-out',str(STATE/'server.csr')])
    (STATE/'extensions.cnf').write_text(f'subjectAltName=DNS:localhost,DNS:openbao.poc,IP:{bi}\nextendedKeyUsage=serverAuth\n')
    run(['openssl','x509','-req','-in',str(STATE/'server.csr'),'-CA',str(STATE/'ca.crt'),
         '-CAkey',str(STATE/'ca.key'),'-CAcreateserial','-days','7','-extfile',str(STATE/'extensions.cnf'),'-out',str(STATE/'server.crt')])
    for f in STATE.iterdir(): os.chmod(f,0o600)
    hcl='''ui = false
storage "pebbledb" { path = "/data/storage" }
audit "file" "file" {
 options {
  file_path = "/data/audit.json"
 }
}
listener "tcp" {
 address = "0.0.0.0:8200"
 tls_cert_file = "/tls/tls.crt"
 tls_key_file = "/tls/tls.key"
 tls_min_version = "tls12"
}
'''
    hard={'allowPrivilegeEscalation':False,'readOnlyRootFilesystem':True,'capabilities':{'drop':['ALL']}}
    apply(B,[obj('Secret','bao-tls',type='kubernetes.io/tls',data={
        'tls.crt':base64.b64encode((STATE/'server.crt').read_bytes()).decode(),
        'tls.key':base64.b64encode((STATE/'server.key').read_bytes()).decode()}),
        obj('ConfigMap','bao-config',data={'server.hcl':hcl}),
        obj('Deployment','openbao',{'replicas':1,'selector':{'matchLabels':{'app':'openbao'}},
          'template':{'metadata':{'labels':{'app':'openbao'}},'spec':{
            'automountServiceAccountToken':False,
            'securityContext':{'runAsNonRoot':True,'runAsUser':1000,'runAsGroup':1000,'fsGroup':1000,'seccompProfile':{'type':'RuntimeDefault'}},
            'containers':[{'name':'openbao','image':BAO_IMAGE,'command':['bao'],'args':['server','-config=/config/server.hcl'],
              'ports':[{'containerPort':8200}], 'securityContext':hard,
              'resources':{'requests':{'cpu':'100m','memory':'128Mi'},'limits':{'cpu':'500m','memory':'512Mi'}},
              'volumeMounts':[{'name':'tls','mountPath':'/tls','readOnly':True},{'name':'config','mountPath':'/config','readOnly':True},
                              {'name':'data','mountPath':'/data'},{'name':'tmp','mountPath':'/tmp'}]}],
            'volumes':[{'name':'tls','secret':{'secretName':'bao-tls'}},{'name':'config','configMap':{'name':'bao-config'}},
                       {'name':'data','emptyDir':{}},{'name':'tmp','emptyDir':{}}]}}}),
        obj('Service','openbao',{'type':'NodePort','selector':{'app':'openbao'},'ports':[{'port':8200,'targetPort':8200,'nodePort':30200}]})], 'bao.json')
    k(B,'-n','poc','rollout','status','deployment/openbao','--timeout=240s')
    apply(A,[obj('ServiceAccount','reviewer',automountServiceAccountToken=False),
        obj('ClusterRole','poc-tokenreview',namespace=None,rules=[{'apiGroups':['authentication.k8s.io'],
            'resources':['tokenreviews'],'verbs':['create']}]),
        obj('ClusterRoleBinding','poc-tokenreview',namespace=None,
            roleRef={'apiGroup':'rbac.authorization.k8s.io','kind':'ClusterRole','name':'poc-tokenreview'},
            subjects=[{'kind':'ServiceAccount','name':'reviewer','namespace':'poc'}])], 'reviewer.json')
    for c in (A,B):
        apply(c,[obj('ConfigMap','probe',data={'probe.py':(ROOT/'scripts/probe.py').read_text()}),
                 obj('ConfigMap','poc-ca',data={'ca.crt':(STATE/'ca.crt').read_text()})],c+'-probe.json')
    p=forward()
    try:
        result=api('sys/init',{'secret_shares':1,'secret_threshold':1})
        secure_write(STATE/'bootstrap.json',json.dumps(result))
        api('sys/unseal',{'key':result['keys'][0]})
        root=result['root_token']
        devices=api('sys/audit',token=root)
        if 'file/' not in devices.get('data',devices):
            raise RuntimeError('Auditoria declarativa file/ não habilitada; revise server.hcl')
        api('sys/mounts/secret',{'type':'kv','options':{'version':'2'}},root)
        api('secret/data/app/config',{'data':{'message':'dado-ficticio-da-poc'}},root)
        api('secret/data/other/config',{'data':{'message':'outro-dado-ficticio'}},root)
        api('sys/policies/acl/app-reader',{'policy':'path "secret/data/app/config" { capabilities = ["read"] }'},root)
        api('sys/auth/cluster-a',{'type':'kubernetes'},root)
        configure_auth(root,ai)
        api('auth/cluster-a/role/reader',{'bound_service_account_names':['reader'],
            'bound_service_account_namespaces':['poc'],'audience':'openbao',
            'token_policies':['app-reader'],'token_ttl':'300s','token_max_ttl':'300s'},root)
        api('auth/cluster-a/role/reader-expiry',{'bound_service_account_names':['reader'],
            'bound_service_account_namespaces':['poc'],'audience':'openbao',
            'token_policies':['app-reader'],'token_ttl':'30s','token_max_ttl':'30s'},root)
    finally: p.terminate(); p.wait()
    print('SETUP concluído. Execute: python3 scripts/lab.py test')

def configure_auth(root,ai):
    reviewer=k(A,'-n','poc','create','token','reviewer','--duration=1h').strip()
    cfg=json.loads(k(A,'config','view','--raw','--minify','-o','json'))
    ca=base64.b64decode(cfg['clusters'][0]['cluster']['certificate-authority-data']).decode()
    api('auth/cluster-a/config',{'kubernetes_host':f'https://{ai}:6443',
        'kubernetes_ca_cert':ca,'token_reviewer_jwt':reviewer,'disable_local_ca_jwt':True},root)

def job(cluster,name,mode,serviceaccount='reader',audience='openbao'):
    network=json.loads((STATE/'network.json').read_text())
    url=f'https://{network["b"]}:30200' if cluster==A else 'https://openbao.poc:8200'
    pod={'serviceAccountName':serviceaccount,'automountServiceAccountToken':False,'restartPolicy':'Never',
        'securityContext':{'runAsNonRoot':True,'runAsUser':1000,'runAsGroup':1000,'seccompProfile':{'type':'RuntimeDefault'}},
        'containers':[{'name':'probe','image':'python:3.12-alpine','command':['python','/probe/probe.py'],
            'env':[{'name':'BAO_URL','value':url},{'name':'MODE','value':mode}],
            'securityContext':{'allowPrivilegeEscalation':False,'readOnlyRootFilesystem':True,'capabilities':{'drop':['ALL']}},
            'resources':{'requests':{'cpu':'50m','memory':'32Mi'},'limits':{'cpu':'200m','memory':'128Mi'}},
            'volumeMounts':[{'name':n,'mountPath':p,'readOnly':True} for n,p in [('probe','/probe'),('ca','/ca'),('identity','/identity')]]}],
        'volumes':[{'name':'probe','configMap':{'name':'probe'}},{'name':'ca','configMap':{'name':'poc-ca'}},
            {'name':'identity','projected':{'sources':[{'serviceAccountToken':{'path':'token','audience':audience,'expirationSeconds':600}}]}}]}
    if cluster==B:
        # SAN DNS e endereço direto do Service; evita depender de DNS no teste de bloqueio.
        svc=json.loads(k(B,'-n','poc','get','svc','openbao','-o','json'))['spec']['clusterIP']
        pod['hostAliases']=[{'ip':svc,'hostnames':['openbao.poc']}]
    apply(cluster,[obj('Job',name,{'backoffLimit':0,'activeDeadlineSeconds':120,
        'template':{'metadata':{'labels':{'app':'probe','access':'allowed' if mode!='blocked' else 'blocked'}},'spec':pod}})],name+'.json')
    for _ in range(90):
        result=json.loads(k(cluster,'-n','poc','get','job',name,'-o','json'))['status']
        if result.get('succeeded') or result.get('failed'): break
        time.sleep(2)
    logs=k(cluster,'-n','poc','logs','job/'+name)
    (EVIDENCE/(name+'.log')).write_text(logs)
    passed=bool(result.get('succeeded'))
    print(name, 'PASS' if passed else 'FAIL')
    return passed

def policies():
    net=json.loads((STATE/'network.json').read_text())
    pods=json.loads(k(B,'-n','poc','get','pods','-l','app=openbao','-o','json'))
    bao_ip=pods['items'][0]['status']['podIP']
    # Os limites de SNAT/NodePort são discutidos na documentação. O teste decide, não a presença do YAML.
    apply(A,[obj('NetworkPolicy','probe-egress',{'podSelector':{'matchLabels':{'app':'probe'}},'policyTypes':['Egress'],
        'egress':[{'to':[{'ipBlock':{'cidr':net['b']+'/32'}},{'ipBlock':{'cidr':bao_ip+'/32'}}],
                   'ports':[{'protocol':'TCP','port':30200},{'protocol':'TCP','port':8200}]}]})], 'a-policy.json')
    apply(B,[obj('NetworkPolicy','bao-ingress',{'podSelector':{'matchLabels':{'app':'openbao'}},'policyTypes':['Ingress','Egress'],
        'egress':[{'to':[{'ipBlock':{'cidr':net['a']+'/32'}}],'ports':[{'protocol':'TCP','port':6443}]}],
        'ingress':[{'from':[{'ipBlock':{'cidr':net['a']+'/32'}}, {'ipBlock':{'cidr':net['b']+'/32'}},
                    {'podSelector':{'matchLabels':{'app':'probe','access':'allowed'}}}],
                    'ports':[{'protocol':'TCP','port':8200}]}]})], 'b-policy.json')

def test():
    if not (STATE/'bootstrap.json').exists(): raise RuntimeError('Execute setup primeiro')
    EVIDENCE.mkdir(exist_ok=True)
    # Permite repetir a suíte após atualizar o cliente do pacote.
    for cluster in (A,B):
        apply(cluster,[obj('ConfigMap','probe',data={'probe.py':(ROOT/'scripts/probe.py').read_text()})],cluster+'-probe-current.json')
    root=json.loads((STATE/'bootstrap.json').read_text())['root_token']
    p=forward()
    try: configure_auth(root,json.loads((STATE/'network.json').read_text())['a'])
    finally: p.terminate(); p.wait()
    # Retira somente políticas desta POC para baseline repetível.
    k(A,'-n','poc','delete','networkpolicy','probe-egress','--ignore-not-found=true')
    k(B,'-n','poc','delete','networkpolicy','bao-ingress','--ignore-not-found=true')
    stamp=str(int(time.time()))
    results={}
    results['baseline_connection']=job(A,'baseline-'+stamp,'authorized')
    # Um probe marcado como blocked deve alcançar o serviço ANTES da política.
    results['baseline_unrestricted']=job(B,'baseline-net-'+stamp,'bad-ca')
    policies()
    for name,cluster,mode,sa,audience in [
        ('authorized',A,'authorized','reader','openbao'),
        ('wrong-sa',A,'wrong-sa','outsider','openbao'),
        ('wrong-audience',A,'wrong-audience','reader','wrong'),
        ('expired',A,'expired','reader','openbao'),
        ('leaked-token',A,'leaked-token','reader','openbao'),
        ('attack-chain',A,'attack-chain','reader','openbao'),
        ('tls-ca',A,'bad-ca','reader','openbao')]:
        results[name]=job(cluster,name+'-'+stamp,mode,sa,audience)
    if results['authorized']:
        results['network-denied']=job(B,'network-denied-'+stamp,'blocked')
    else:
        results['network-denied']=False
        print('Bloqueio não comprovado: serviço autorizado não ficou acessível.')
    for sa,verb,resource,expected in [('reader','get','secrets','no'),('reviewer','create','tokenreviews.authentication.k8s.io','yes'),
                                      ('reviewer','get','secrets','no'),('reader','create','pods','no'),
                                      ('reader','create','clusterrolebindings.rbac.authorization.k8s.io','no')]:
        answer=subprocess.run(['kubectl','--context','kind-'+A,'auth','can-i',verb,resource,
            '--as=system:serviceaccount:poc:'+sa,'-n','poc'],text=True,capture_output=True)
        if answer.returncode not in (0,1) or answer.stdout.strip() not in ('yes','no'):
            raise RuntimeError('Falha na verificação RBAC: '+answer.stderr[:500])
        response=answer.stdout.strip()
        results['rbac-'+sa+'-'+verb+'-'+resource]=(response==expected)
    audit=k(B,'-n','poc','exec','deployment/openbao','--','cat','/data/audit.json')
    results['audit_present']=bool(audit.strip())
    # Guarda só contagem; audit bruto pode conter metadados de identidade/IP.
    report={'executed_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'results':results,
        'audit_lines':len(audit.splitlines()),'limitations':['NodePort pode mascarar origem; validar SNAT/CNI.',
            'Bloqueio demonstrado com Pod local no cluster B; não prova isolamento entre workloads externos.']}
    (EVIDENCE/'results.json').write_text(json.dumps(report,indent=2))
    print('Evidências em evidence/results.json. Tokens não são incluídos.')
    if not all(results.values()): raise RuntimeError('Há testes FAIL; consulte docs/05-operacao.md')

def cleanup():
    for c in (A,B):
        if (STATE/(c+'.owned')).exists():
            run(['kind','delete','cluster','--name',c],capture=False)
            (STATE/(c+'.owned')).unlink()
    # Não remove automaticamente credenciais e evidências: operador revisa .state.
    print('Clusters pertencentes a esta POC removidos. Apague .state quando não precisar mais do laboratório.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('action',choices=['setup','test','cleanup','preflight'])
    args=parser.parse_args()
    try: globals()[args.action]()
    except Exception as e:
        print('ERRO:',str(e),file=sys.stderr); sys.exit(1)
