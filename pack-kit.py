"""
Package the kit into a distributable folder + zip.

Whitelist-based (never blacklist): only known-good files ship, so private
videos, out/, node_modules and .env can never leak into a build.

Usage:
  python scripts/pack-kit.py            -> dist/video-editor-kit/ + dist/video-editor-kit-<version>.zip
  python scripts/pack-kit.py --no-zip   -> folder only
"""
import argparse
import json
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

# directories copied whole (relative to kit root)
DIRS = [
    ".claude",            # skills / commands / agents / workflows
    "scripts",
    "src",
    "public/sfx",         # sound effects: forgetting these broke past handoffs
    "goldens",            # per-family reference stills (drift detector)
]
# individual files
FILES = [
    "CLAUDE.md",
    "README.md",
    "HUONG-DAN.md",
    "CHANGELOG.md",
    "package.json",
    "package-lock.json",
    "requirements.txt",
    "remotion.config.ts",
    "tsconfig.json",
    ".gitignore",
]
# junk that never ships even inside whitelisted dirs
EXCLUDE_PARTS = {"__pycache__", ".venv", "node_modules"}
EXCLUDE_SUFFIXES = {".pyc"}

# fail-loud checks: a build missing any of these is broken by definition
MUST_EXIST = [
    ".claude/skills/video-editor/SKILL.md",
    ".claude/skills/video-editor/references/style-menu.md",
    ".claude/skills/video-editor/references/workflow-talking-head.md",
    ".claude/skills/video-editor/references/workflow-broll-hook.md",
    ".claude/commands/biz-edit-video.md",
    ".claude/commands/biz-broll-video.md",
    ".claude/commands/biz-help.md",
    ".claude/agents/video-finder.md",
    ".claude/agents/video-critic.md",
    ".claude/workflows/video-review.js",
    "CLAUDE.md",
    "scripts/run-pipeline.py",
    "scripts/run-broll-pipeline.py",
    "scripts/doctor.py",
    "public/sfx",
]


def should_skip(p: Path) -> bool:
    return any(part in EXCLUDE_PARTS for part in p.parts) or p.suffix in EXCLUDE_SUFFIXES


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-zip", action="store_true")
    a = ap.parse_args()

    missing = [m for m in MUST_EXIST if not (ROOT / m).exists()]
    if missing:
        print("PACK FAILED - required paths missing:")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)

    version = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["version"]
    dest = DIST / "video-editor-kit"
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    n = 0
    for d in DIRS:
        src = ROOT / d
        if not src.exists():
            print(f"PACK FAILED - whitelist dir missing: {d}")
            sys.exit(1)
        for f in src.rglob("*"):
            if f.is_dir() or should_skip(f):
                continue
            rel = f.relative_to(ROOT)
            out = dest / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, out)
            n += 1
    for name in FILES:
        src = ROOT / name
        if not src.exists():
            print(f"PACK FAILED - whitelist file missing: {name}")
            sys.exit(1)
        shutil.copy2(src, dest / name)
        n += 1
    # empty dirs users need on first run
    for d in ("public/raw", "public/music", "out"):
        (dest / d).mkdir(parents=True, exist_ok=True)

    sfx_count = len(list((dest / "public/sfx").glob("*")))
    if sfx_count == 0:
        print("PACK FAILED - public/sfx is empty in the build")
        sys.exit(1)

    print(f"Packed {n} files -> {dest}  (sfx: {sfx_count}, version {version})")

    if not a.no_zip:
        zip_path = DIST / f"video-editor-kit-{version}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for f in dest.rglob("*"):
                if f.is_file():
                    z.write(f, f.relative_to(DIST))
        print(f"Zip -> {zip_path} ({zip_path.stat().st_size // 1024} KB)")

    print("\nUser install steps (put these in your delivery message):")
    print("  1. Unzip anywhere, e.g. C:\\video-editor-kit")
    print("  2. Inside the folder: npm install && pip install -r requirements.txt")
    print("  3. Open Claude Code IN the folder: claude")
    print("  4. Type: /biz-help (checks the machine + shows the menu)")


if __name__ == "__main__":
    main()
