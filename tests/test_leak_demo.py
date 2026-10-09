import importlib.util,pathlib,unittest,json
spec=importlib.util.spec_from_file_location('leak_demo',pathlib.Path(__file__).resolve().parents[1]/'scripts/leak_demo.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class LogDemoTest(unittest.TestCase):
    def test_baseline_exposes_and_controlled_log_removes_markers(self):
        result=module.evaluate()
        self.assertTrue(result['baseline_exposes_marker'])
        self.assertFalse(result['controlled_log_exposes_marker'])
        self.assertEqual(result['result'],'PASS')
    def test_marker_inside_allowed_field_is_not_forwarded(self):
        record={'event':'login','status':'TOKEN_FICTICIO_INVALIDO'}
        output=json.dumps(module.operational_log(record))
        self.assertFalse(module.exposed(output))
        self.assertEqual(module.operational_log(record)['status'],'invalid')

if __name__=='__main__':unittest.main()
