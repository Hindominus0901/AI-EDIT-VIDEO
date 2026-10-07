import copy,sys,tempfile,unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from style_packages import asset_identity,validate_plan,reject_unimplemented_package

class StylePackageGuards(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.public=Path(self.tmp.name)
        (self.public/'clip.mp4').write_bytes(b'path-only fixture; no decode claim')
        for name,color in [('book.png','red'),('pen.png','blue'),('voice.png','green')]:Image.new('RGB',(20,20),color).save(self.public/name)
        self.package={'id':'R16','version':'1.0.0','policy':{'allowedLayouts':['speaker','collage'],
          'supportedPlanAspects':['9:16','16:9'],'maxGraphicOccupancy':.35,'maxGraphicBeatsPerMinute':2,
          'maxConsecutiveGraphicBeats':2,'callbackMinGapMs':30000,'maxCaptionWords':5,'maxSfxPerMinute':4}}
        self.plan={'stylePackage':'R16','packageVersion':'1.0.0','status':'reviewed','clip':'clip.mp4',
          'timebase':'edited-clip','durationMs':120000,'aspect':'9:16','brief':{'audience':'Người học','promise':'Luyện nói','takeaway':'Đọc to'},
          'assets':[{'id':f'a{i}','file':f,'meaning':'Phần cụ thể của bài tập'} for i,f in enumerate(['book.png','pen.png','voice.png'])],
          'beats':[self.beat('b1',10000)],'captions':[],'audio':{'sfx':[]}}
    def tearDown(self):self.tmp.cleanup()
    def beat(self,bid,start):
        return {'id':bid,'startMs':start,'endMs':start+3000,'role':'example','layout':'collage',
          'meaning':'Minh họa ba phần của bài tập','conceptId':'practice','referenceEvent':'R16 collage entrance',
          'assetIds':['a0','a1','a2'],'entryMs':750,'exitMs':250}
    def report(self,p=None):return validate_plan(p or self.plan,self.package,self.public)
    def codes(self,p=None):return {e['code'] for e in self.report(p)['errors']}
    def test_unique_assets_pass_and_explicit_callback_is_limited(self):
        self.assertTrue(self.report()['ok'])
        b=self.beat('b2',75000);b.update(callbackOf='b1',callbackReason='Nhắc lại chính bài tập ở kết bài')
        self.plan['beats'].append(b);self.assertTrue(self.report()['ok'])
        b3=self.beat('b3',110000);b3.update(callbackOf='b1',callbackReason='Again')
        self.plan['beats'].append(b3);self.assertIn('asset-reuse',self.codes())
    def test_renaming_same_picture_does_not_evade_reuse(self):
        Image.open(self.public/'book.png').save(self.public/'renamed.bmp')
        self.plan['assets'].append({'id':'alias','file':'renamed.bmp','meaning':'A different filename'})
        b=self.beat('b2',75000);b['assetIds']=['alias','a1','a2'];self.plan['beats'].append(b)
        self.assertIn('asset-reuse',self.codes())
        self.assertEqual(asset_identity(self.plan['assets'][0],self.public),asset_identity(self.plan['assets'][-1],self.public))
    def test_distinct_panels_are_distinct_but_same_panel_repeats(self):
        im=Image.new('RGB',(40,20),'red');im.paste('blue',(20,0,40,20));im.save(self.public/'strip.png')
        a={'file':'strip.png','crop':[0,0,.5,1]};b={'file':'strip.png','crop':[.5,0,.5,1]}
        self.assertNotEqual(asset_identity(a,self.public),asset_identity(b,self.public))
        with self.assertRaises(ValueError):asset_identity({'file':'strip.png','crop':[0,0,0,1]},self.public)
    def test_new_filenames_do_not_hide_dense_collage_burst(self):
        self.plan['beats']=[self.beat('b1',10000),self.beat('b2',25000),self.beat('b3',40000)]
        self.assertIn('graphic-frequency',self.codes())
    def test_wrong_style_long_caption_and_invalid_times_fail(self):
        self.plan['beats'][0]['layout']='circle-comparison';self.plan['beats'][0]['entryMs']=4000
        self.plan['captions']=[{'startMs':0,'endMs':1000,'text':'Đây là một câu phụ đề quá dài'}]
        self.assertTrue({'layout','motion-hold','caption-length'}<=self.codes())
    def test_blank_form_and_generic_renderer_cannot_claim_ready(self):
        self.plan['status']='draft';self.plan['beats']=[]
        self.assertTrue({'draft','beats'}<=self.codes())
        with self.assertRaisesRegex(ValueError,'refusing silent'):reject_unimplemented_package(self.plan)
        reject_unimplemented_package({'premiumSet':'studio'})
    def test_callback_cannot_change_concept_or_skip_gap(self):
        b=self.beat('b2',20000);b.update(callbackOf='b1',callbackReason='Recall',conceptId='different')
        self.plan['beats'].append(b);self.assertIn('asset-reuse',self.codes())
    def test_file_must_stay_inside_public(self):
        self.plan['assets'][0]['file']='../outside.png';self.assertIn('asset-file',self.codes())

if __name__=='__main__':unittest.main()
