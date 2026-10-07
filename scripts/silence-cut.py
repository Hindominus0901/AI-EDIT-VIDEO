"""Natural pacing: preserve speech, shorten only verified long silence.
--protected JSON contains [[startMs,endMs], ...] for intentional pauses.
--plan-only emits a reviewable source-to-output map without encoding video.
"""
import argparse,json,re,subprocess,tempfile,shutil
from pathlib import Path
from pacing import plan_pacing,remap
ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--clip',default='raw/talkinghead.mp4')
    ap.add_argument('--max-gap-ms',type=int,default=900)
    ap.add_argument('--pad-ms',type=int,default=160,help='breathing handle on each side')
    ap.add_argument('--no-fillers',action='store_true',help='compatibility: fillers are always preserved')
    ap.add_argument('--out-dir',default=str(ROOT/'out'))
    ap.add_argument('--public-dir',default=str(ROOT/'public'))
    ap.add_argument('--protected')
    ap.add_argument('--plan-only',action='store_true')
    a=ap.parse_args(); out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=True)
    clip=Path(a.public_dir)/a.clip
    transcript=json.loads((out/'transcript.json').read_text(encoding='utf-8-sig'))
    probe=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(clip)],capture_output=True,text=True,check=True)
    duration=float(json.loads(probe.stdout)['format']['duration'])*1000
    # Transcript can slightly exceed mux duration due to STT rounding; reject any
    # real discrepancy instead of silently clipping words.
    if transcript['words'] and transcript['words'][-1]['endMs'] > duration+50:
        raise ValueError('Transcript exceeds source duration')
    duration=max(duration,max((w['endMs'] for w in transcript['words']),default=0))
    detect=subprocess.run(['ffmpeg','-hide_banner','-i',str(clip),'-vn','-af','silencedetect=noise=-38dB:d=0.9','-f','null','-'],capture_output=True,text=True,check=True)
    silences=[];start=None
    for kind,value in re.findall(r'silence_(start|end):\s*([0-9.]+)',detect.stderr):
        if kind=='start':start=float(value)*1000
        elif start is not None:silences.append([start,float(value)*1000]);start=None
    if start is not None:silences.append([start,duration])
    protected=json.loads(Path(a.protected).read_text(encoding='utf-8-sig')) if a.protected else []
    p=plan_pacing(transcript['words'],duration,silences,protected,a.max_gap_ms,2*a.pad_ms)
    words=remap(transcript['words'],p['spans'])
    assert len(words)==len(transcript['words']), 'A cut intersects speech; refusing to render'
    total=p['durationMs']
    report={**p,'originalSec':duration/1000,'tightSec':total/1000,
            'removedSec':round((duration-total)/1000,3),'removedPct':round((1-total/duration)*100,2),
            'segments':len(p['spans']),'wordsKept':len(words),'wordsOriginal':len(words),
            'policy':'natural-verified-silence-v1'}
    (out/'cut-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'transcript-tight.json').write_text(json.dumps({**transcript,'durationSec':total/1000,'words':words},ensure_ascii=False,indent=2),encoding='utf-8')
    if a.plan_only:
        print(f'PLAN: {len(p["cuts"])} safe silence cuts; {len(p["review"])} review markers');return
    dest=out/'tight.mp4'
    if not p['cuts']:
        shutil.copyfile(clip,dest) # no cuts = no avoidable encode
    else:
        # Single encode avoids per-segment AAC padding and repeated video loss.
        filters=[];labels=[]
        for i,(s,e) in enumerate(p['spans']):
            d=(e-s)/1000
            filters += [f'[0:v]trim=start={s/1000}:end={e/1000},setpts=PTS-STARTPTS[v{i}]',
                        f'[0:a]atrim=start={s/1000}:end={e/1000},asetpts=PTS-STARTPTS,afade=t=in:d=0.005,afade=t=out:st={max(0,d-.005)}:d=0.005[a{i}]']
            labels.append(f'[v{i}][a{i}]')
        filters.append(''.join(labels)+f'concat=n={len(labels)}:v=1:a=1[v][a]')
        with tempfile.TemporaryDirectory() as tmp:
            graph=Path(tmp)/'filter.txt';graph.write_text(';\n'.join(filters),encoding='utf-8')
            subprocess.run(['ffmpeg','-y','-v','error','-i',str(clip),'-/filter_complex',str(graph),'-map','[v]','-map','[a]','-c:v','libx264','-crf','16','-preset','fast','-c:a','aac','-b:a','192k','-movflags','+faststart',str(dest)],check=True)
    print(f'OK: {report["originalSec"]:.2f}s -> {report["tightSec"]:.2f}s; all {len(words)} words preserved')

if __name__=='__main__':main()

