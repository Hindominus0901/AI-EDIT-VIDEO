import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from pacing import plan_pacing, remap

def w(text,s,e): return {'text':text,'startMs':s,'endMs':e}

class PacingTests(unittest.TestCase):
    def test_transcript_gap_without_audio_evidence_preserved(self):
        p=plan_pacing([w('Hello',0,300),w('world',3000,3400)],4000)
        self.assertEqual(p['spans'], [[0,4000]])
    def test_sentence_breath_kept_and_timestamps_follow_actual_cut(self):
        words=[w('Done.',0,400),w('Next',2400,2700)]
        p=plan_pacing(words,3000,[(400,2400)])
        self.assertEqual(p['cuts'][0]['retainedMs'],760)
        mapped=remap(words,p['spans'])
        self.assertEqual(mapped[1]['startMs']-mapped[0]['endMs'],760)
        self.assertEqual(len(mapped),2)
    def test_emotional_pause_protected(self):
        p=plan_pacing([w('Wait.',0,200),w('Yes',3000,3400)],3500,[(200,3000)],[(0,3200)])
        self.assertFalse(p['cuts'])
    def test_vietnamese_connectives_and_emphatic_repeats_not_deleted(self):
        words=[w('ý',0,100),w('là',100,200),w('rất',200,300),w('rất',300,400),w('tốt',400,500)]
        p=plan_pacing(words,600)
        self.assertEqual(remap(words,p['spans']),words)
        self.assertEqual(p['review'][0]['kind'],'repeat')
    def test_empty_transcript_keeps_source(self):
        self.assertEqual(plan_pacing([],2000)['spans'],[[0,2000]])
    def test_short_pauses_and_hesitations_kept(self):
        words=[w('um',100,300),w('yes',800,1000)]
        self.assertFalse(plan_pacing(words,1100,[(300,800)])['cuts'])
    def test_invalid_timestamps_rejected(self):
        with self.assertRaises(ValueError): plan_pacing([w('bad',800,100)],1000)

if __name__=='__main__': unittest.main()
