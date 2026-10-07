import sys,unittest,tempfile,json,copy
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from reviewed_cuts import compile_cuts
from clean_edit import compose_clean
from clean_media import media_tracks
from pipeline_common import render_final

class UpgradeTests(unittest.TestCase):
    def test_preview_bounds_frames_and_preserves_edl_and_existing_output(self):
        with tempfile.TemporaryDirectory() as d,patch('pipeline_common.subprocess.run') as run:
            out=Path(d);edl={'source':{'durationSec':20},'format':{'w':1080,'h':1920,'fps':30},'style':{'layout':'focused'},'tracks':{'captions':[]}}
            original=json.dumps(edl);(out/'edl.json').write_text(original)
            (out/'preview-9x16.mp4').write_bytes(b'old')
            result=render_final(out,aspects=['9:16'],preview_seconds=3)
            self.assertEqual(result.name,'preview-9x16-v2.mp4')
            self.assertIn('--frames=0-89',run.call_args.args[0])
            self.assertEqual((out/'edl.json').read_text(),original)
            self.assertEqual((out/'preview-9x16.mp4').read_bytes(),b'old')

    def test_cut_mapping_preserves_negation_and_source(self):
        transcript={'durationSec':5,'words':[{'text':'không','startMs':100,'endMs':500},{'text':'spam','startMs':600,'endMs':900},{'text':'lặp','startMs':2000,'endMs':2300},{'text':'niềm tin','startMs':4000,'endMs':4500}]}
        before=copy.deepcopy(transcript)
        timeline,mapped=compile_cuts(transcript,{'status':'reviewed','keep':[{'startMs':0,'endMs':1000,'reason':'Giữ phủ định'},{'startMs':3900,'endMs':4700,'reason':'Giữ kết luận'}]})
        self.assertEqual([w['text'] for w in mapped['words']],['không','spam','niềm tin'])
        self.assertEqual(mapped['words'][-1]['startMs'],1100)
        self.assertAlmostEqual(timeline['durationSec'],1.8)
        self.assertFalse(timeline['joins'][0]['listeningReviewed']);self.assertEqual(transcript,before)

    def test_midword_cut_rejected(self):
        with self.assertRaisesRegex(ValueError,'spoken word'):
            compile_cuts({'durationSec':2,'words':[{'text':'không','startMs':100,'endMs':600}]},{'status':'reviewed','keep':[{'startMs':300,'endMs':1000,'reason':'test'}]})

    def test_contiguous_captions_hold_and_camera_reaches_edl(self):
        with tempfile.TemporaryDirectory() as d,patch('clean_edit.subprocess.run') as probe:
            probe.return_value.stdout=json.dumps({'streams':[{'width':720,'height':1280}]})
            plan={'timebase':'edited-clip','premiumSet':'editorial-c','moments':[],'captions':[{'text':'Giữ lại điều hay','startMs':0,'endMs':1000},{'text':'Và kể tiếp câu chuyện','startMs':1100,'endMs':2500}],'camera':[{'startMs':0,'endMs':3000,'scale':1.09}]}
            edl,_=compose_clean({'durationSec':4,'words':[]},plan,'raw/a.mp4',Path(d),'9:16')
            self.assertEqual(edl['tracks']['captions'][0]['endMs'],1100)
            self.assertEqual(edl['tracks']['captions'][1]['motion']['entry'],'hold')
            self.assertEqual(edl['tracks']['effects'][0]['scale'],1.09)
            self.assertEqual(edl['style']['premiumSet'],'editorial-c')

    def test_broll_ends_before_file_ends(self):
        with patch('clean_media.subprocess.run') as probe:
            probe.return_value.stdout=json.dumps({'streams':[{'codec_type':'video','duration':'3'}],'format':{}})
            with self.assertRaisesRegex(ValueError,'exceeds'):
                media_tracks({'broll':[{'src':'a.mp4','startMs':0,'endMs':3000,'offsetSec':1}]},4000,Path('.'),lambda _,n:n)

    def test_camera_overlap_and_nan_rejected(self):
        for cues in [[{'startMs':0,'endMs':3000},{'startMs':2000,'endMs':4000}],[{'startMs':0,'endMs':2000,'scale':float('nan')}]]:
            with self.assertRaises(ValueError):media_tracks({'camera':cues},5000,Path('.'),lambda _,n:n)
if __name__=='__main__':unittest.main()
