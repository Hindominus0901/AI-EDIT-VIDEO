"""A synthetic Vietnamese render check. Never uses customer footage or STT."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from clean_edit import compose_clean
from pipeline_common import write_edl_guarded, render_final

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser(description='Xuất thử dấu Việt bằng nguồn tổng hợp, không dùng video cá nhân.')
    p.add_argument('--aspect',choices=['9:16','16:9','both'],default='9:16')
    p.add_argument('--prepare-only',action='store_true',help='Chỉ tạo nguồn và EDL thử.')
    a=p.parse_args()
    source=ROOT/'public/samples/setup-test.mp4'
    source.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x253c33:s=960x540:r=30',
                    '-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-t','3','-c:v','libx264',
                    '-pix_fmt','yuv420p','-c:a','aac','-shortest',str(source)],check=True)
    out=ROOT/'out/setup-smoke'
    # A separate revision avoids overwriting a prior diagnostic result.
    base=out;revision=2
    while out.exists():
        out=base.with_name(f'{base.name}-{revision}');revision+=1
    out.mkdir(parents=True)
    plan={'clip':'samples/setup-test.mp4','timebase':'edited-clip','premiumSet':'studio',
          'captions':[{'startMs':100,'endMs':1450,'text':'Bắt đầu từ điều nhỏ'},
                      {'startMs':1500,'endMs':2900,'text':'Dựng video rõ ý hơn'}],
          'moments':[{'sec':.1,'keyword':'điều nhỏ','role':'hook','sound':False}]}
    edl,report=compose_clean({'durationSec':3,'words':[]},plan,plan['clip'],ROOT/'public','9:16' if a.aspect=='both' else a.aspect)
    write_edl_guarded(out,edl)
    (out/'host-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'check.json').write_text(json.dumps({'synthetic':True,'speechRecognitionTested':False,'editReport':report},ensure_ascii=False,indent=2),encoding='utf-8')
    if not a.prepare_only:
        render_final(out,aspects=['9:16','16:9'] if a.aspect=='both' else [a.aspect])
        for video in out.glob('final-*.mp4'):
            subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
    print(f'SMOKE_OUTPUT={out}')
    print('Nguồn thử tổng hợp; không kiểm thử nhận giọng hay chất lượng biên tập nội dung thật.')

if __name__=='__main__':
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8')
    main()
