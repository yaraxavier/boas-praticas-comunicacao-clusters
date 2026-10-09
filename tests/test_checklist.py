import contextlib, importlib.util, io, json, pathlib, sys, tempfile, unittest

SPEC=importlib.util.spec_from_file_location('checklist',pathlib.Path(__file__).resolve().parents[1]/'scripts/checklist.py')
module=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(module)

class ChecklistTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.root=pathlib.Path(self.temp.name)
        self.original=(module.ROOT,module.CATALOG,module.FORM)
        module.ROOT=self.root; module.CATALOG=self.root/'catalog.json'; module.FORM=self.root/'evidence/form.json'
        module.CATALOG.write_text(json.dumps([{'id':'BP01','priority':'P0'}]))
        self.argv=sys.argv[:]
    def tearDown(self):
        module.ROOT,module.CATALOG,module.FORM=self.original; sys.argv=self.argv; self.temp.cleanup()
    def invoke(self,action):
        sys.argv=['checklist.py',action]
        with contextlib.redirect_stdout(io.StringIO()): module.main()
    def test_init_preserves_pending_and_refuses_overwrite(self):
        self.invoke('init'); before=module.FORM.read_text()
        self.assertEqual(json.loads(before)['checks'][0]['status'],'pendente')
        with self.assertRaises(SystemExit): self.invoke('init')
        self.assertEqual(module.FORM.read_text(),before)
    def test_pending_p0_is_not_treated_as_approved(self):
        self.invoke('init')
        with self.assertRaises(SystemExit) as e: self.invoke('report')
        self.assertEqual(e.exception.code,1)
    def test_missing_evidence_fails_even_when_claimed_conforming(self):
        self.invoke('init'); data=json.loads(module.FORM.read_text())
        data['checks'][0].update(status='conforme',evidence='missing.log',owner='Revisor',checked_at='2026-10-08')
        module.FORM.write_text(json.dumps(data))
        with self.assertRaises(SystemExit): self.invoke('report')
    def test_documentary_record_accepts_existing_evidence(self):
        self.invoke('init'); (self.root/'result.log').write_text('resultado para revisão humana')
        data=json.loads(module.FORM.read_text())
        data['checks'][0].update(status='conforme',evidence='result.log',owner='Revisor',checked_at='2026-10-08')
        module.FORM.write_text(json.dumps(data)); self.invoke('report')

if __name__=='__main__': unittest.main()
