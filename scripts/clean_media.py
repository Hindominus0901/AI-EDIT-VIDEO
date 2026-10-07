"""Validate explicit edited-time camera/B-roll plans before rendering. No asset generation."""
import math, subprocess, json

def finite(value,name):
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
        raise ValueError(f'{name} must be a finite number')
    return value

def media_tracks(plan,duration_ms,public_dir,checked_asset):
    effects=[];broll=[]
    for key,target in [('camera',effects),('broll',broll)]:
        last=-1
        for cue in plan.get(key,[]):
            a=finite(cue['startMs'],key+'.startMs');b=finite(cue['endMs'],key+'.endMs')
            if not 0<=a<b<=duration_ms or a<last:raise ValueError(f'{key}: ordered, non-overlapping edited-time windows required')
            last=b
            if key=='camera':
                scale=finite(cue.get('scale',1.08),'camera.scale');kind=cue.get('type','zoom')
                if kind not in ('zoom','punch-in') or not 1<=scale<=1.15 or b-a<800:
                    raise ValueError('Camera: zoom/punch-in, scale 1–1.15, and at least 800ms required')
                target.append(dict(type=kind,startMs=a,endMs=b,scale=scale))
            else:
                src=checked_asset(public_dir,cue['src']);offset=finite(cue.get('offsetSec',0),'broll.offsetSec');fade=finite(cue.get('fadeSec',.23),'broll.fadeSec')
                if offset<0 or not 0<=fade<=1:raise ValueError('B-roll offset/fade out of range')
                probe=json.loads(subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(public_dir/src)],capture_output=True,text=True,check=True).stdout)
                video=next((s for s in probe['streams'] if s['codec_type']=='video'),None)
                if video is None:raise ValueError('B-roll requires video footage')
                available=float(video.get('duration') or probe['format']['duration'])
                if offset+(b-a)/1000>available+.001:raise ValueError('B-roll window exceeds available footage; looping is not implicit')
                if any(x['src']==src for x in broll):raise ValueError('Repeated B-roll source: choose distinct footage or author a reviewed custom sequence')
                target.append(dict(startMs=a,endMs=b,src=src,prompt=cue.get('reason','Provided real footage'),offsetSec=offset,fadeSec=fade))
    return effects,broll
