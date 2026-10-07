"""Generate synthetic creator fixtures; optionally render each. No customer media shipped."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from clean_edit import compose_clean, write_srt
from pipeline_common import write_edl_guarded, write_project_context

ROOT=Path(__file__).resolve().parents[1]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--render',action='store_true')
    ap.add_argument('--clip',default='samples/setup-test.mp4')
    ap.add_argument('--captions',type=Path,help='Existing SRT; never runs STT')
    ap.add_argument('--duration',type=float,default=3)
    ap.add_argument('--out-dir',type=Path,default=ROOT/'out/creator-demo')
    a=ap.parse_args()
    captions=[]
    if a.captions:
        def stamp(s):
            h,m,rest=s.split(':');sec,ms=rest.split(',')
            return (int(h)*3600+int(m)*60+int(sec))*1000+int(ms)
        for block in a.captions.read_text(encoding='utf-8-sig').strip().split('\n\n'):
            lines=block.splitlines()
            if len(lines)<3:continue
            start,stop=map(stamp,lines[1].split(' --> '))
            if stop<=a.duration*1000:captions.append({'startMs':start,'endMs':stop,'text':' '.join(lines[2:])})
    else:
        captions=[{'startMs':0,'endMs':a.duration*1000,'text':'Giữ lại điều quan trọng'}]
    for mode in ('iman','hormozi','martell'):
        folder=a.out_dir/mode;folder.mkdir(parents=True,exist_ok=True)
        if (folder/'host-plan.json').exists():
            raise ValueError('Choose a fresh demo directory to preserve existing work')
        duration=round(a.duration*1000)
        scenes=[{'id':'open','startMs':0,'endMs':duration,'layout':'speaker','meaning':'Giữ lời nguồn','reason':'Kiểm tra chữ và giọng trên nguồn thật'}]
        if a.captions and a.duration>=19.2:
            scenes=[{**scenes[0],'endMs':12067},
                    {'id':'analogy','startMs':12067,'endMs':16533,'layout':'compare','title':'Một bài giữa biển nội dung',
                     'meaning':'Một bài mới so với lượng nội dung đã có','reason':'Làm rõ phép so sánh của người nói',
                     'items':[{'text':'Nội dung đang có','atMs':0},{'text':'Một bài vừa đăng','atMs':750}]},
                    {'id':'close','startMs':16533,'endMs':duration,'layout':'statement','title':'Thêm muối vào biển.',
                     'meaning':'Phép ví von kết đoạn','reason':'Nhường toàn bộ khung hình cho câu chốt'}]
            if mode=='hormozi':scenes[1]['motion']='cut'
            if mode=='martell':
                scenes[1].update(layout='steps',title='Điều đang xảy ra',items=[{'text':'Tạo thêm một bài','atMs':0},{'text':'Thả vào biển nội dung','atMs':2600}])
            if mode=='iman':scenes[1]={'id':'hold','startMs':12067,'endMs':16533,'layout':'speaker','meaning':'Dẫn vào phép ví von','reason':'Giữ mặt, tạo khoảng yên trước câu chốt'}
        plan={'clip':a.clip,'timebase':'edited-clip','creatorStyle':mode,
              'story':{'audience':'Người làm nội dung','premise':'Spam AI không tạo khác biệt','payoff':'Hiểu giới hạn của việc chỉ tăng số lượng'},
              'captions':captions,'scenes':scenes,'framing':{'fit':'contain','focusX':50,'focusY':50},
              'moments':[]}
        if a.captions:
            plan['moments']=[{'sec':2.9,'keyword':'spam','role':'emphasis','reason':'Từ khóa của lời cảnh báo'}]
            plan['music']={'src':'music/cc0/contemplation.mp3','volume':.025,'fadeOutSec':1,'loop':True}
            plan['audioCues']=[{'startMs':16533,'endMs':duration,'gain':.2,'reason':'Hạ nền để giữ trọng tâm ở phép ví von'}]
        edl,report=compose_clean({'durationSec':a.duration,'words':[]},plan,a.clip,ROOT/'public','9:16')
        (folder/'host-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
        write_edl_guarded(folder,edl);write_srt(folder/'captions.srt',edl['tracks']['captions'])
        write_project_context(folder,edl)
        (folder/'edit-plan.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        (folder/'props.json').write_text(json.dumps({'edl':edl},ensure_ascii=False),encoding='utf-8')
        subprocess.run([sys.executable,str(ROOT/'scripts/validate-edl-risk.py'),str(folder/'edl.json')],check=True)
        if a.render:
            subprocess.run(['npx.cmd' if sys.platform=='win32' else 'npx','remotion','render','Reel',str(folder/'preview.mp4'),
                '--props='+str(folder/'props.json'),'--scale=.5','--concurrency=3','--crf=20','--x264-preset=fast'],cwd=ROOT,check=True)


if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
