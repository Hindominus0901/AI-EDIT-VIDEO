import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('pure_edit_audit', ROOT/'scripts/pure-edit-audit.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PureEditAuditTests(unittest.TestCase):
    def edl(self):
        return {'source':{'durationSec':12},'tracks':{
            'captions':[{'text':'Một ý thật rõ','startMs':0,'endMs':1200,'motion':{'entry':'rise'}},
                        {'text':'Bằng chứng cụ thể','startMs':1500,'endMs':2600,'motion':{'entry':'hold'}}],
            'graphics':[{'startMs':4000,'endMs':6000}], 'broll':[], 'effects':[], 'sfx':[]}}

    def test_accepts_restrained_edit(self):
        report = module.audit(self.edl())
        self.assertTrue(report['ok'])
        self.assertEqual(report['counts']['graphics'], 1)

    def test_rejects_caption_overflow_and_competing_visuals(self):
        edl = self.edl()
        edl['tracks']['captions'][0]['text'] = 'Một câu phụ đề có quá nhiều chữ'
        edl['tracks']['broll'] = [{'startMs':5000,'endMs':7000}]
        report = module.audit(edl)
        self.assertFalse(report['ok'])
        self.assertTrue(any('words' in item for item in report['failures']))
        self.assertTrue(any('overlaps' in item for item in report['failures']))


if __name__ == '__main__':
    unittest.main()
