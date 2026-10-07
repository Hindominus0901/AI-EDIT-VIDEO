"""Compile host-reviewed speech selections onto one frame-aligned timebase.

Never decides which words are dispensable. It flags joins for listening review.
"""
import argparse,json,math,subprocess
from pathlib import Path

def compile_cuts(transcript,plan,fps=30):
    if plan.get('status')!='reviewed':raise ValueError('A host-reviewed selection plan is required')
    if isinstance(fps,bool) or not isinstance(fps,int) or not 1<=fps<=120:raise ValueError('Invalid FPS')
    duration=transcript['durationSec']*1000
    if not math.isfinite(duration) or duration<=0:raise ValueError('Invalid source duration')
    words=transcript['words'];spans=[];cursor=0;last=0
    for c in plan['keep']:
        a,b=c['startMs'],c['endMs']
        if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) for v in (a,b)):raise ValueError('Non-finite selection')
        a=round(a*fps/1000);b=round(b*fps/1000)
        if not 0<=a<b<=round(duration*fps/1000) or a<last:raise ValueError('Selections must be ordered, non-overlapping and in source bounds')
        if not c.get('reason','').strip():raise ValueError('Each retained section needs an editorial reason')
        for boundary in (a*1000/fps,b*1000/fps):
            if any(w['startMs']+35<boundary<w['endMs']-35 for w in words):raise ValueError(f'Cut at {boundary:.1f}ms crosses a spoken word; revise boundary')
        spans.append(dict(sourceIn=a,sourceOut=b,editIn=cursor,editOut=cursor+b-a,reason=c['reason']));cursor+=b-a;last=b
    if not spans:raise ValueError('No retained source')
    mapped=[];joins=[]
    for i,s in enumerate(spans):
        a,b=s['sourceIn']*1000/fps,s['sourceOut']*1000/fps;shift=s['editIn']*1000/fps-a
        kept=[w for w in words if a<=(w['startMs']+w['endMs'])/2<b]
        mapped.extend({**w,'startMs':round(max(a,w['startMs'])+shift),'endMs':round(min(b,w['endMs'])+shift)} for w in kept)
        if i:
            prev=spans[i-1];pa,pb=prev['sourceIn']*1000/fps,prev['sourceOut']*1000/fps
            before=[w['text'] for w in words if pa<=(w['startMs']+w['endMs'])/2<pb][-8:]
            joins.append(dict(editMs=round(s['editIn']*1000/fps),before=' '.join(before),after=' '.join(w['text'] for w in kept[:8]),listeningReviewed=False))
    return dict(fps=fps,durationSec=cursor/fps,segments=spans,joins=joins),{**transcript,'durationSec':cursor/fps,'words':mapped}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--transcript',required=True);ap.add_argument('--plan',required=True);ap.add_argument('--out-dir',required=True);ap.add_argument('--fps',type=int,default=30);ap.add_argument('--render',action='store_true');a=ap.parse_args()
    timeline,transcript=compile_cuts(json.loads(Path(a.transcript).read_text(encoding='utf-8-sig')),json.loads(Path(a.plan).read_text(encoding='utf-8-sig')),a.fps)
    out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=False)
    (out/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'transcript.json').write_text(json.dumps(transcript,ensure_ascii=False,indent=2),encoding='utf-8')
    if a.render:
        filters=[];labels=[]
        for i,s in enumerate(timeline['segments']):
            start,end=s['sourceIn']/a.fps,s['sourceOut']/a.fps;duration=end-start
            filters.extend([f'[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS,fps={a.fps}[v{i}]',f'[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS,afade=t=in:d=0.004,afade=t=out:st={max(0,duration-.004)}:d=0.004[a{i}]'])
            labels.append(f'[v{i}][a{i}]')
        filters.append(''.join(labels)+f'concat=n={len(labels)}:v=1:a=1[v][a]')
        graph=out/'cut-filter.txt';graph.write_text(';\n'.join(filters))
        subprocess.run(['ffmpeg','-v','error','-i',a.source,'-filter_complex',graph.read_text(),'-map','[v]','-map','[a]','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out/'source-cut.mp4')],check=True)
    print(f'CUT_OUTPUT={out.resolve()}')
if __name__=='__main__':main()
