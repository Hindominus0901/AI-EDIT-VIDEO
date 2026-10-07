"""
Full local-first pipeline orchestrator.

Default path uses no API key:
  STT: local faster-whisper
  Edit planning: current host AI (clean), optional CLI (legacy only)
  Media/render helpers: ffmpeg, OpenCV, Remotion

Usage:
  python scripts/run-pipeline.py raw/project/clip.mp4 --out-dir out/project --llm offline --render
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
PUBLIC = ROOT / "public"
OUT = ROOT / "out"
PY = sys.executable


def run(cmd, **kw):
    print(f"  $ {' '.join(str(c) for c in cmd)}")
    return subprocess.run(cmd, check=True, **kw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip", help="path relative to public/, e.g. raw/talkinghead.mp4")
    ap.add_argument("--out-dir", default="out", help="project output folder; relative to the engine")
    ap.add_argument("--keep-silence", action="store_true", help="skip silence removal")
    ap.add_argument("--max-gap-ms", type=int, default=900)
    ap.add_argument("--protected-pauses", help="JSON [[startMs,endMs], ...] in source time; never shorten these pauses")
    ap.add_argument("--smart", action="store_true", help="deeper multi-pass critique where provider supports it")
    ap.add_argument("--edit-style", choices=['clean','legacy'], default='clean')
    ap.add_argument("--aspect", choices=['source','9:16','16:9','both'], default='source')

    ap.add_argument("--stt", default="local",
                    choices=["local", "faster-whisper"],
                    help="speech-to-text provider; default is local faster-whisper")
    ap.add_argument("--stt-model", default="small", help="faster-whisper local model size")
    ap.add_argument("--language", default="vi")
    # cpu default: 'auto' hard-crashes on machines with a GPU but no cuDNN
    ap.add_argument("--device", default="cpu", help="cpu (safe default) | cuda | auto")
    ap.add_argument("--compute-type", default="auto")
    ap.add_argument("--no-cache", action="store_true",
                    help="fresh content run: do not read or write the transcript cache")

    ap.add_argument("--llm", default="offline", choices=["claude-cli", "offline", "prefed"],
                    help="Legacy reasoning provider. Clean uses a host-written --plan or local fallback; no nested model call.")
    ap.add_argument("--plan", default=None,
                    help="host-written reasoning JSON for --llm prefed (default out/host-plan.json)")
    ap.add_argument("--model", default="local", help="reserved for local CLI providers")
    ap.add_argument("--force-regen", action="store_true",
                    help="overwrite out/edl.json even if it has manual edits")
    ap.add_argument("--render", action="store_true",
                    help="render out/final.mp4 with Remotion after the pipeline")
    ap.add_argument("--open", action="store_true",
                    help="open the rendered video when done (implies --render)")
    a = ap.parse_args()
    out = Path(a.out_dir)
    if not out.is_absolute():
        out = ROOT / out
    out = out.resolve()
    if a.open:
        a.render = True

    clip_abs = (PUBLIC / a.clip).resolve()
    if not clip_abs.is_relative_to(PUBLIC.resolve()) or not clip_abs.is_file():
        print(f"ERROR: clip not found: {clip_abs}"); sys.exit(1)
    out.mkdir(parents=True, exist_ok=True)

    # a new clip must not silently clobber the previous project's work
    from pipeline_common import archive_previous_project
    archive_previous_project(out, Path(a.clip).stem)

    # Cache ORIGINAL word timestamps by media content and STT configuration.
    # Never cache the tightened transcript: every edit starts in source time.
    digest = hashlib.sha256()
    with clip_abs.open('rb') as media:
        for block in iter(lambda: media.read(1024 * 1024), b''):
            digest.update(block)
    digest.update(json.dumps([a.stt, a.stt_model, a.language, a.device,
                              a.compute_type, 'source-transcript-v1']).encode())
    digest.update((SCRIPTS / 'transcribe.py').read_bytes())
    cache_dir = ROOT / '.cache' / 'transcripts'
    cached = cache_dir / (digest.hexdigest() + '.json')
    cache_hit = cached.exists() and not a.no_cache
    if not cache_hit:
        print("[1] Extract audio...")
        run(["ffmpeg", "-y", "-i", str(clip_abs), "-ar", "16000", "-ac", "1",
             str(out / "audio.wav")], capture_output=True)
    print(f"[2] Transcribe ({a.stt}){' - cached' if cache_hit else ' - fresh/no-cache' if a.no_cache else ''}...")
    stt_cmd = [
        PY, str(SCRIPTS / "transcribe.py"), str(out / "audio.wav"),
        "--out", str(out / "transcript.json"),
        "--engine", a.stt,
        "--local-model", a.stt_model,
        "--language", a.language,
        "--device", a.device,
        "--compute-type", a.compute_type,
    ]
    if cache_hit:
        shutil.copyfile(cached, out / 'transcript.json')
    else:
        run(stt_cmd)
        if not a.no_cache:
            cache_dir.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(out / 'transcript.json', cached)
    shutil.copyfile(out / 'transcript.json', out / 'transcript-source.json')

    final_clip = a.clip
    if not a.keep_silence:
        print("[3] Natural pacing: verified silence only...")
        cut_cmd = [PY, str(SCRIPTS / "silence-cut.py"), "--clip", a.clip,
                   "--max-gap-ms", str(a.max_gap_ms), "--out-dir", str(out)]
        if a.protected_pauses:
            cut_cmd += ['--protected', a.protected_pauses]
        run(cut_cmd)
        shutil.copy(out / "transcript-tight.json", out / "transcript.json")
        # Preserve the project namespace even when two clips share a basename.
        tight_name = f"{Path(a.clip).stem}-tight.mp4"
        tight_pub = clip_abs.parent / tight_name
        shutil.copy(out / "tight.mp4", tight_pub)
        final_clip = tight_pub.relative_to(PUBLIC.resolve()).as_posix()
        report = json.loads((out / "cut-report.json").read_text(encoding="utf-8"))
        print(f"    cut {report['removedSec']}s ({report['removedPct']}%), "
              f"{report['segments']} jump-cuts -> {final_clip}")
    else:
        print("[3] Silence-cut SKIPPED (--keep-silence)")

    print("[3b] Face-zone detection (local OpenCV)...")
    run([PY, str(SCRIPTS / "detect-face-zones.py"), final_clip, "--out-dir", str(out)])

    print(f"[4] Generate EDL ({a.llm})...")
    edl_cmd = [
        PY, str(SCRIPTS / "generate-edl.py"),
        "--clip", final_clip,
        "--out-dir", str(out),
        "--llm", a.llm,
        "--model", a.model,
        "--edit-style", a.edit_style,
        "--aspect", '9:16' if a.aspect=='both' else a.aspect,
    ]
    if a.plan:
        edl_cmd += ["--plan", a.plan]
    if a.smart:
        edl_cmd.append("--smart")
    if a.force_regen:
        edl_cmd.append("--force-regen")
    run(edl_cmd)

    if not a.render:
        print("\n[5] DONE. Render with:")
        print(f'    python scripts/render-edit.py --out-dir "{out}" --aspect {a.aspect}')
        return

    # guard: never render an edl.json that belongs to a different clip —
    # a leftover working copy from another project would silently win
    edl = json.loads((out / "edl.json").read_text(encoding="utf-8"))
    edl_clip = edl.get("source", {}).get("clip")
    if edl_clip != final_clip:
        print(f"LOI: out/edl.json thuoc clip khac ({edl_clip}), khong phai {final_clip}.")
        print("  Dung --force-regen de sinh lai EDL cho clip nay,")
        print("  hoac render EDL do rieng: npm run render:edl")
        sys.exit(1)

    print("[5] Render (Remotion)...")
    from pipeline_common import render_final
    final_mp4 = render_final(out,open_after=a.open,aspects=['9:16','16:9'] if a.aspect=='both' else [a.aspect])
    print(f"\n[6] DONE -> {final_mp4}")


if __name__ == "__main__":
    main()

