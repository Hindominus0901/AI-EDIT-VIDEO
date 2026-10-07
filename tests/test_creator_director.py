import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from clean_edit import compose_clean
from creator_director import validate_director


def plan():
    return {'creatorStyle':'martell','timebase':'edited-clip',
            'story':{'audience':'Người làm nội dung','premise':'Ít nhưng rõ','payoff':'Một ý có ích'},
            'captions':[{'startMs':0,'endMs':1000,'text':'Không cần làm nhiều'}],
            'scenes':[{'id':'a','startMs':0,'endMs':4000,'layout':'steps','title':'Ba bước',
                       'meaning':'Một quy trình','reason':'Xây theo lời',
                       'items':[{'text':'Chọn ý','atMs':0},{'text':'Chứng minh','atMs':1700}]}]}


class CreatorTests(unittest.TestCase):
    def compile(self,p,root):
        with patch('clean_edit.subprocess.run') as probe:
            probe.return_value.stdout=json.dumps({'streams':[{'width':1080,'height':1920}]})
            return compose_clean({'durationSec':5,'words':[]},p,'source.mp4',root,'9:16')

    def test_all_profiles_reach_renderer_and_preserve_input_negation(self):
        with tempfile.TemporaryDirectory() as d:
            for name in ('iman','hormozi','martell'):
                p=plan();p['creatorStyle']=name;before=copy.deepcopy(p)
                edl,report=self.compile(p,Path(d))
                self.assertEqual(edl['style']['layout'],'creator')
                self.assertEqual(edl['director']['profile'],name)
                self.assertEqual(edl['tracks']['captions'][0]['text'],'Không cần làm nhiều')
                self.assertEqual(edl['tracks']['graphics'],[])
                self.assertEqual(report['nestedModelCalls'],0)
                self.assertEqual(p,before)

    def test_unknown_profile_or_missing_story_never_silently_falls_back(self):
        for changes in ({'creatorStyle':'unknown'},{'creatorStyle':''},{'story':{}},{'timebase':'source'},{'premiumSet':'studio'},{'scenes':[]}):
            with self.assertRaises(ValueError):self.compile({**plan(),**changes},Path('.'))

    def test_timeline_and_reveal_errors(self):
        for change in ('overlap','nan','late-item','missing-reason'):
            p=plan()
            if change=='overlap':p['scenes'].append({**p['scenes'][0],'id':'b','startMs':3000,'endMs':5000})
            if change=='nan':p['scenes'][0]['startMs']=float('nan')
            if change=='late-item':p['scenes'][0]['items'][1]['atMs']=3900
            if change=='missing-reason':p['scenes'][0]['reason']=''
            with self.assertRaises(ValueError):self.compile(p,Path('.'))

    def test_repeated_evidence_needs_meaningful_callback_and_safe_path(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'a.png').write_bytes(b'image')
            p=plan();s={'id':'first','startMs':0,'endMs':2000,'layout':'evidence','title':'Tài liệu',
                       'image':'a.png','assetSource':'Người dùng cung cấp','meaning':'Bằng chứng','reason':'Đối chiếu'}
            p['scenes']=[s,{**s,'id':'second','startMs':2500,'endMs':4500}]
            with self.assertRaisesRegex(ValueError,'callback'):self.compile(p,root)
            p['scenes'][1].update(callbackTo='first',callbackReason='Trở lại bằng chứng để kết luận')
            self.compile(p,root)
            p['scenes'][0]['image']='../outside.png'
            with self.assertRaises(ValueError):self.compile(p,root)

    def test_music_cue_without_track_rejected(self):
        p=plan();p['audioCues']=[{'startMs':0,'endMs':1000,'gain':0,'reason':'Khoảng nghỉ'}]
        with self.assertRaisesRegex(ValueError,'music'):self.compile(p,Path('.'))

if __name__=='__main__':unittest.main()
