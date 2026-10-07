"""Deterministic creator finishing: mild source LUT, dialogue cleanup and ducked music.

Keeps the camera original untouched. Run `grade` before the Remotion render and
`mix` on a muted render. All paths are explicit; this never invokes a model.
"""
import argparse
import json
from pathlib import Path
import subprocess


def run(*args):
    subprocess.run([str(a) for a in args], check=True)


def lut(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    lines = ['TITLE "Warm neutral editorial"', 'LUT_3D_SIZE 17', 'DOMAIN_MIN 0 0 0', 'DOMAIN_MAX 1 1 1']
    def channel(x, lift, gain):
        return max(0.0, min(1.0, ((x-0.5)*1.055+0.5+lift)*gain))
    for b in range(17):
        for g in range(17):
            for r in range(17):
                lines.append(f'{channel(r/16,.002,1.012):.6f} {channel(g/16,.001,1.003):.6f} {channel(b/16,0,.986):.6f}')
    path.write_text('\n'.join(lines)+'\n', encoding='ascii')


def grade(args):
    source, out, curve = Path(args.source), Path(args.out), Path(args.lut)
    if not source.is_file(): raise FileNotFoundError(source)
    lut(curve)
    out.parent.mkdir(parents=True, exist_ok=True)
    run('ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,
        '-t',args.seconds,'-vf',f"lut3d=file='{curve.as_posix()}'",
        '-an','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p',out)


def mix(args):
    video, voice, music, out = map(Path,(args.render,args.voice,args.music,args.out))
    for path in (video,voice,music):
        if not path.is_file(): raise FileNotFoundError(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    duration=float(args.seconds)
    # A measured music bed enters below speech; sidechain follows the actual voice.
    graph=(
        f'[1:a]atrim=0:{duration},asetpts=PTS-STARTPTS,highpass=f=75,lowpass=f=14000,'
        'acompressor=threshold=0.12:ratio=2.5:attack=10:release=160:makeup=1.15,'
        'loudnorm=I=-16:TP=-2:LRA=7,asplit=2[voice][voicekey];'
        f'[2:a]atrim=0:{duration},asetpts=PTS-STARTPTS,volume=0.22,'
        f'afade=t=in:st=0:d=0.5,afade=t=out:st={max(0,duration-1.2)}:d=1.2[music];'
        '[music][voicekey]sidechaincompress=threshold=0.025:ratio=7:attack=20:release=420[bed];'
        f'[0:a]atrim=0:{duration},asetpts=PTS-STARTPTS,volume=0.65[sfx];'
        '[voice][bed][sfx]amix=inputs=3:duration=first:normalize=0,'
        'alimiter=limit=0.89:attack=5:release=70,volume=0.9[a]'
    )
    run('ffmpeg','-hide_banner','-loglevel','error','-y','-i',video,'-i',voice,'-i',music,
        '-filter_complex',graph,'-map','0:v:0','-map','[a]','-c:v','copy','-c:a','aac',
        '-b:a','256k','-ar','48000','-t',duration,'-movflags','+faststart',out)
    probe=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type',
        '-of','json',str(out)],capture_output=True,text=True,check=True)
    data=json.loads(probe.stdout)
    if {s['codec_type'] for s in data['streams']} != {'video','audio'}:
        raise RuntimeError('Finished output must include video and audio')
    print(json.dumps({'out':str(out),'duration':data['format']['duration'],
        'look':'warm-neutral-17.cube','voice':'highpass + compressor + loudnorm',
        'music':'real-voice sidechain duck + fades'},ensure_ascii=False))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    sp=p.add_subparsers(dest='command',required=True)
    a=sp.add_parser('grade');a.add_argument('--source',required=True);a.add_argument('--out',required=True)
    a.add_argument('--lut',required=True);a.add_argument('--seconds',required=True,type=float)
    a=sp.add_parser('mix');a.add_argument('--render',required=True);a.add_argument('--voice',required=True)
    a.add_argument('--music',required=True);a.add_argument('--out',required=True);a.add_argument('--seconds',required=True,type=float)
    args=p.parse_args()
    {'grade':grade,'mix':mix}[args.command](args)
