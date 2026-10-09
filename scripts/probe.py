"""Executado dentro de um Job; nunca imprime tokens ou valores de segredos."""
import json, os, ssl, time, urllib.request, urllib.error

base = os.environ['BAO_URL']
ctx = ssl.create_default_context(cafile=os.environ.get('PROBE_CA','/ca/ca.crt'))
mode = os.environ.get('MODE', 'authorized')
auth_mount = os.environ.get('AUTH_MOUNT', 'cluster-a')
own_path = os.environ.get('OWN_PATH', 'secret/data/app/config')
foreign_path = os.environ.get('FOREIGN_PATH', 'secret/data/other/config')

def request(path, data=None, token=None, context=ctx):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['X-Vault-Token'] = token
    req = urllib.request.Request(base+'/v1/'+path,
        data=json.dumps(data).encode() if data is not None else None, headers=headers)
    try:
        with urllib.request.urlopen(req, context=context, timeout=8) as r:
            raw = r.read()
            return r.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        return e.code, {}

def check(name, condition):
    print(json.dumps({'test': name, 'result': 'PASS' if condition else 'FAIL'}), flush=True)
    if not condition:
        raise SystemExit(1)

if mode == 'blocked':
    # A confirmação de serviço saudável é feita pelo runner antes deste Job.
    try:
        request('sys/health')
    except (urllib.error.URLError, TimeoutError, OSError):
        check('network_denied', True)
    else:
        check('network_denied', False)
elif mode == 'bad-ca':
    try:
        request('sys/health', context=ssl.create_default_context())
    except urllib.error.URLError as e:
        check('untrusted_ca_rejected', isinstance(e.reason, ssl.SSLCertVerificationError))
    else:
        check('untrusted_ca_rejected', False)
else:
    jwt = open(os.environ.get('PROBE_JWT','/identity/token')).read().strip()
    status, result = request('auth/'+auth_mount+'/login', {'role': 'reader-expiry' if mode=='expired' else 'reader', 'jwt': jwt})
    if mode in ('wrong-sa', 'wrong-audience'):
        check(mode+'_rejected', status in (400, 403))
    else:
        check('identity_accepted', status == 200)
        token = result['auth']['client_token']
        check('short_ttl', 0 < result['auth']['lease_duration'] <= 300)
        status, _ = request(own_path, token=token)
        check('allowed_read', status == 200)
        if mode == 'leaked-token':
            # Atacante simulado já possui a credencial válida da aplicação.
            # A leitura própria continua possível: risco residual esperado.
            check('leaked_token_own_scope_still_accessible', status == 200)
        if mode == 'attack-chain':
            # Cadeia controlada após comprometimento de um consumidor; nenhuma exploração real.
            for endpoint, label in [('sys/mounts','mount_admin_denied'),
                                    ('sys/audit','audit_admin_denied'),
                                    ('auth/token/create','create_arbitrary_token_denied')]:
                payload={} if endpoint=='auth/token/create' else None
                denied, _ = request(endpoint, payload, token=token)
                check(label, denied == 403)
        if mode == 'expired':
            time.sleep(result['auth']['lease_duration'] + 5)
            status, _ = request(own_path, token=token)
            check('expired_token_denied', status == 403)
            raise SystemExit(0)
        status, _ = request(foreign_path, token=token)
        check('foreign_path_denied', status == 403)
        status, _ = request(own_path, {'data': {'x': 'ficticio'}}, token=token)
        check('write_denied', status == 403)
        status, _ = request('auth/token/revoke-self', {}, token=token)
        check('revoke_self', status in (200, 204))
        status, _ = request(own_path, token=token)
        check('revoked_token_denied', status == 403)
