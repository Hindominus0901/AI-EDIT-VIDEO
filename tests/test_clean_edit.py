import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from clean_edit import build_clean_captions,validate_captions,compose_clean
from pipeline_common import write_edl_guarded


def words(text):
    return [{'text':w,'startMs':i*300,'endMs':(i+1)*300} for i,w in enumerate(text.split())]


class CleanEditTests(unittest.TestCase):
    def test_partition_retains_negation_and_every_word(self):
        source=words('Tôi không nói rằng bạn phải giỏi mọi thứ để bắt đầu xây thương hiệu cá nhân.')
        original=copy.deepcopy(source)
        caps=build_clean_captions(source)
        self.assertEqual(' '.join(c['text'] for c in caps),' '.join(w['text'] for w in source))
        self.assertTrue(all(len(c['text'].split())<=5 for c in caps))
        self.assertEqual(source,original)
        validate_captions(caps,source[-1]['endMs'])

    def test_known_phrase_not_broken_to_hit_five(self):
        caps=build_clean_captions(words('Bạn có thể xây thương hiệu cá nhân ngay từ một ngách nhỏ.'))
        self.assertTrue(any('thương hiệu' in c['text'] for c in caps))
        self.assertTrue(any('ngách nhỏ' in c['text'] for c in caps))

    def test_caption_overlap_and_out_of_bounds_fail(self):
        with self.assertRaises(ValueError):
            validate_captions([{'text':'Một câu','startMs':0,'endMs':1200},{'text':'Câu khác','startMs':1100,'endMs':1400}],1500)
        with self.assertRaises(ValueError):
            validate_captions([{'text':'Một câu','startMs':0,'endMs':1600}],1500)

    def compose(self,plan,captions=None):
        caps=captions or [{'text':'Bằng chứng thật','startMs':4000,'endMs':6000},
                         {'text':'Phản hồi trực tiếp','startMs':7000,'endMs':9000}]
        transcript={'durationSec':12,'words':[]}
        with tempfile.TemporaryDirectory() as tmp,patch('clean_edit.subprocess.run') as probe:
            probe.return_value.stdout=json.dumps({'streams':[{'width':1280,'height':720}]})
            return compose_clean(transcript,{'timebase':'edited-clip','captions':caps,**plan},'raw/test.mp4',Path(tmp),'9:16')

    def test_moments_require_nearby_matching_words_and_space(self):
        edl,report=self.compose({'moments':[
            {'sec':4,'keyword':'Bằng chứng','role':'proof','asset':'proof','sound':True},
            {'sec':7,'keyword':'Phản hồi','role':'example','asset':'chat','sound':True},
            {'sec':10,'keyword':'không tồn tại','role':'close'}]})
        self.assertEqual(len(edl['tracks']['graphics']),1)
        self.assertEqual(edl['tracks']['graphics'][0]['endMs'],6000)
        self.assertEqual(len(edl['tracks']['sfx']),1)
        self.assertEqual(edl['tracks']['effects'],[])
        self.assertEqual(edl['tracks']['transitions'],[])
        self.assertEqual(edl['style']['layout'],'focused')
        self.assertEqual(report['nestedModelCalls'],0)
        self.assertEqual(edl['format']['w'],1080)

    def test_fallback_does_not_match_time_inside_sometimes(self):
        edl,_=self.compose({},[{'text':'sometimes we just listen','startMs':0,'endMs':2000}])
        self.assertNotIn('keyword',edl['tracks']['captions'][0]['motion'])
        self.assertFalse(edl['tracks']['graphics'])

    def test_premium_sets_preserve_story_timing_and_baseline(self):
        plan={'moments':[{'sec':4,'keyword':'Bằng chứng','role':'proof','asset':'proof'}]}
        baseline,_=self.compose(plan)
        self.assertNotIn('premiumSet',baseline['style'])
        for name in ('studio','paper','mono'):
            edl,report=self.compose({**plan,'premiumSet':name})
            self.assertEqual(edl['source'],baseline['source'])
            self.assertEqual(edl['tracks']['graphics'],baseline['tracks']['graphics'])
            self.assertEqual([(c['text'],c['startMs'],c['endMs']) for c in edl['tracks']['captions']],
                             [(c['text'],c['startMs'],c['endMs']) for c in baseline['tracks']['captions']])
            self.assertEqual(report['premiumSet'],name)
            self.assertEqual(report['nestedModelCalls'],0)
        with self.assertRaisesRegex(ValueError,'Unknown premiumSet'):
            self.compose({'premiumSet':'typo'})

    def test_pure_edit_expands_tiny_look_choice_without_reference_reads(self):
        edl,report=self.compose({'pureEdit':True,'look':'direct','moments':[]})
        self.assertEqual(edl['style']['premiumSet'],'mono')
        self.assertEqual(edl['style']['layout'],'standard')
        self.assertEqual(report['pureEdit']['runtimeReferenceReads'],0)
        self.assertEqual(report['pureEdit']['hostPlanFields'],['pureEdit','look','moments'])
        with self.assertRaisesRegex(ValueError,'Unknown pure-edit look'):
            self.compose({'pureEdit':True,'look':'neon-everything'})

    def test_new_photo_pair_requires_two_real_assets(self):
        with tempfile.TemporaryDirectory() as tmp,patch('clean_edit.subprocess.run') as probe:
            probe.return_value.stdout=json.dumps({'streams':[{'width':1280,'height':720}]})
            public=Path(tmp)
            (public/'one.jpg').write_bytes(b'fixture')
            plan={'timebase':'edited-clip','premiumSet':'paper',
                  'captions':[{'text':'Hình ảnh có chiều sâu','startMs':4000,'endMs':6000}],
                  'moments':[{'sec':4,'keyword':'chiều sâu','role':'example','graphic':'photo-diptych','images':['one.jpg']}]}
            with self.assertRaisesRegex(ValueError,'requires 2'):
                compose_clean({'durationSec':10,'words':[]},plan,'x.mp4',public)
            plan['moments'][0]['images'].append('missing.jpg')
            with self.assertRaisesRegex(ValueError,'Missing local asset'):
                compose_clean({'durationSec':10,'words':[]},plan,'x.mp4',public)
            (public/'missing.jpg').write_bytes(b'fixture')
            edl,_=compose_clean({'durationSec':10,'words':[]},plan,'x.mp4',public)
            self.assertEqual(edl['tracks']['graphics'][0]['motion']['kind'],'photo-diptych')

    def test_curated_uiverse_graphic_expands_from_short_id(self):
        edl,_=self.compose({'pureEdit':True,'look':'quiet','moments':[
            {'sec':4,'keyword':'Bằng chứng','role':'proof','graphic':'ui-notification','label':'Đã xác minh'}]})
        self.assertEqual(edl['tracks']['graphics'][0]['motion'],
                         {'kind':'ui-notification','text':'Đã xác minh'})

    def test_authored_timing_requires_explicit_timebase(self):
        with self.assertRaises(ValueError):
            compose_clean({'durationSec':4,'words':[]},{'captions':[]},'x',Path('.'))

    def test_hand_edits_survive_new_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)
            write_edl_guarded(path,{'version':1})
            (path/'edl.json').write_text('{"manual":true}',encoding='utf-8')
            write_edl_guarded(path,{'version':2})
            self.assertEqual(json.loads((path/'edl.json').read_text()),{'manual':True})
            self.assertEqual(json.loads((path/'edl.generated.json').read_text()),{'version':2})


if __name__=='__main__':unittest.main()
