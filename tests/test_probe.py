"""Teste de integração local do cliente HTTPS; servidor simulado, sem Kubernetes."""
import http.server, json, os, pathlib, ssl, subprocess, tempfile, threading, unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]

class Handler(http.server.BaseHTTPRequestHandler):
    revoked=False
    allowed_read="/v1/secret/data/app/config"
    last_login=None
    def log_message(self,*args): pass
    def reply(self,status,data=None):
        self.send_response(status); self.end_headers()
        if data is not None: self.wfile.write(json.dumps(data).encode())
    def do_POST(self):
        data=json.loads(self.rfile.read(int(self.headers.get('Content-Length',0))) or b'{}')
        if self.path.endswith('/login'):
            type(self).last_login=self.path
            if data.get('jwt')!='fake-authorized-jwt': return self.reply(403,{})
            type(self).revoked=False
            return self.reply(200,{'auth':{'client_token':'fake-sensitive-token','lease_duration':300}})
        if self.path.endswith('/revoke-self'):
            type(self).revoked=True; return self.reply(204)
        return self.reply(403,{})
    def do_GET(self):
        if self.path.endswith('/sys/health'): return self.reply(200,{'sealed':False})
        if self.path==type(self).allowed_read and not type(self).revoked:
            return self.reply(200,{'data':{'data':{'message':'fake-sensitive-value'}}})
        return self.reply(403,{})

class ProbeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(); cls.path=pathlib.Path(cls.temp.name)
        subprocess.run(['openssl','req','-x509','-newkey','rsa:2048','-nodes','-days','1',
            '-subj','/CN=localhost','-addext','subjectAltName=DNS:localhost',
            '-keyout',str(cls.path/'key'),'-out',str(cls.path/'ca')],check=True,capture_output=True)
        cls.server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
        ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(str(cls.path/'ca'),str(cls.path/'key'))
        cls.server.socket=ctx.wrap_socket(cls.server.socket,server_side=True)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True); cls.thread.start()
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join(); cls.temp.cleanup()
    def probe(self,mode='authorized',jwt='fake-authorized-jwt',url=None,extra=None):
        (self.path/'jwt').write_text(jwt)
        env=dict(os.environ,MODE=mode,PROBE_CA=str(self.path/'ca'),PROBE_JWT=str(self.path/'jwt'),
            BAO_URL=url or f'https://localhost:{self.server.server_port}')
        if extra: env.update(extra)
        return subprocess.run(['python3',str(ROOT/'scripts/probe.py')],env=env,text=True,capture_output=True,timeout=15)
    def test_authorization_and_revoke_with_empty_204(self):
        result=self.probe(); self.assertEqual(result.returncode,0,result.stderr)
        for name in ['identity_accepted','allowed_read','foreign_path_denied','write_denied','revoke_self','revoked_token_denied']:
            self.assertIn(name,result.stdout)
        self.assertNotIn('fake-sensitive-token',result.stdout+result.stderr)
        self.assertNotIn('fake-sensitive-value',result.stdout+result.stderr)
    def test_wrong_identity_is_denied(self):
        result=self.probe('wrong-sa','fake-wrong-jwt'); self.assertEqual(result.returncode,0,result.stderr)
    def test_wrong_audience_branch_is_denied(self):
        # Simula apenas HTTP de rejeição; validação criptográfica é responsabilidade do cluster.
        result=self.probe('wrong-audience','fake-wrong-jwt'); self.assertEqual(result.returncode,0,result.stderr)
    def test_untrusted_ca_is_specific_tls_failure(self):
        result=self.probe('bad-ca'); self.assertEqual(result.returncode,0,result.stderr)
    def test_unexpected_denial_fails_positive_test(self):
        result=self.probe('authorized','fake-wrong-jwt'); self.assertNotEqual(result.returncode,0)
        self.assertIn('FAIL',result.stdout)
    def test_leaked_token_exposes_own_scope_but_not_foreign_scope(self):
        result=self.probe('leaked-token'); self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('leaked_token_own_scope_still_accessible',result.stdout)
        self.assertIn('foreign_path_denied',result.stdout)
    def test_controlled_attack_chain_blocks_admin_endpoints(self):
        result=self.probe('attack-chain'); self.assertEqual(result.returncode,0,result.stderr)
        for name in ['mount_admin_denied','audit_admin_denied','create_arbitrary_token_denied']:
            self.assertIn(name,result.stdout)

if __name__=='__main__': unittest.main()
