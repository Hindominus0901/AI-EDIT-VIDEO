"""Build an explicit, private-media-free plugin + engine distribution."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile
import html

ROOT=Path(__file__).resolve().parents[1]
PLUGIN=Path('integrations/video-editor-viet')
CORE_SCRIPTS=['clean_edit.py','detect-face-zones.py','doctor.py','edl_passes.py',
              'generate-edl.py','local_llm.py','make-render-props.mjs','pacing.py',
              'pack-kit.py','pipeline_common.py','render-edit.py','run-pipeline.py',
              'setup-runtime.py','silence-cut.py','smoke-test.py','transcribe.py',
              'user_profile.py','validate-edl-risk.py','style_packages.py','clean_media.py','reviewed_cuts.py','creator_director.py','creator-demo.py','creator-finishing.py','pure-edit-audit.py']
DOCS=['AGENTS.md','BAT-DAU.md','bat-dau.html','HUONG-DAN.md','CLAUDE.md','README.md',
      'CLEAN-AUTO-FLOW.md','package.json','package-lock.json','requirements.txt',
      'requirements-tested.txt','remotion.config.ts','tsconfig.json','.gitignore',
      'DUA-VAO-CHATGPT-WORK.md','STYLE-PREFERENCES.md','CHANGELOG.md',
      'THU-TREN-WORK.md','UPGRADE-1.5.md','UPGRADE-1.6.md','UPGRADE-1.6.1.md']

def selected_files(root=ROOT):
    """Only source and reviewed reusable assets. Never copy .claude memory or goldens."""
    files={Path(p) for p in DOCS}
    files.update(Path('scripts')/p for p in CORE_SCRIPTS)
    files.update(p.relative_to(root) for p in (root/'tests').glob('test_*.py'))
    for folder in ['src','public/fonts/editorial-c','public/graphics/motion-kit','public/images/editorial','public/images/editorial-v4']:
        files.update(p.relative_to(root) for p in (root/folder).rglob('*') if p.is_file())
    files.update(p.relative_to(root) for p in (root/'public/sfx/kenney').glob('*.ogg'))
    files.update([Path('asset-library/cc0-music.json'),Path('asset-library/licenses/Kenney-License.txt'),Path('asset-library/TAI-NGUYEN.md')])
    files.add(Path('asset-library/luts/warm-neutral-17.cube'))
    files.update(p.relative_to(root) for p in (root/'asset-library/editing-library').rglob('*') if p.is_file())
    files.update(p.relative_to(root) for p in (root/'asset-library/uiverse-curated').rglob('*') if p.is_file())
    files.add(Path('asset-library/reference-learning/CREATOR-R01-REVIEW-20260929.md'))
    for item in json.loads((root/'asset-library/cc0-music.json').read_text(encoding='utf-8')):
        if item['license']!='CC0-1.0':raise ValueError('Music whitelist only accepts reviewed CC0 entries.')
        files.update([Path('public')/item['path'],Path(item['licenseEvidence'])])
    for folder in ['premium-kit','motion-kit']:
        for name in ['index.html','README.md','manifest.json']:
            files.add(Path('asset-library')/folder/name)
    files.add(Path('asset-library/premium-kit/premium-sets.mp4'))
    files.add(Path('asset-library/premium-kit/stills/studio-photo.png'))
    files.add(Path('asset-library/motion-kit/motion-catalog.mp4'))
    files.add(Path('asset-library/style-packages/catalog.json'))
    for folder in (root/'asset-library/style-packages').iterdir():
        if folder.is_dir():
            for name in ['package.json','recipe.json','form.json','README.md','source-breakdown.md']:
                p=folder/name
                if p.is_file():files.add(p.relative_to(root))
    for folder in [PLUGIN,Path('.agents/skills')]:
        files.update(p.relative_to(root) for p in (root/folder).rglob('*') if p.is_file())
    files.add(Path('.claude/skills/video-editor/SKILL.md'))
    files.update(p.relative_to(root) for p in (root/'.claude/commands').glob('biz-*.md'))
    for p in files:
        resolved=(root/p).resolve()
        if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():raise ValueError(f'Missing or external package source: {p}')
        if p.is_absolute() or any(part in {'out','raw','.video-editor','.cache','goldens','node_modules','.venv','__pycache__'} for part in p.parts):raise ValueError(f'Private/generated path in package: {p}')
    return sorted(files)

def main():
    ap=argparse.ArgumentParser(description='Đóng gói plugin + engine, không kèm video và hồ sơ cá nhân.')
    ap.add_argument('--no-zip',action='store_true');a=ap.parse_args()
    for canonical in (ROOT/PLUGIN/'skills').iterdir():
        if canonical.is_dir():
            shutil.copytree(canonical,ROOT/'.agents/skills'/canonical.name,dirs_exist_ok=True)
    files=selected_files()
    version=json.loads((ROOT/PLUGIN/'.codex-plugin/plugin.json').read_text(encoding='utf-8'))['version']
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')
    # A new release folder each time: no recursive deletes, no overwritten older kits.
    release=ROOT/'dist'/f'video-editor-viet-{version}-{stamp}'
    dest=release/'video-editor-viet';engine=dest/'engine'
    engine.mkdir(parents=True,exist_ok=False)
    for rel in files:
        target=engine/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,target)
    library=engine/'asset-library/style-packages'
    catalog=json.loads((library/'catalog.json').read_text(encoding='utf-8'))['packages']
    note='21 gói đặc tả và form; không phải 21 preset renderer. Media ref riêng không nằm trong bản phân phối này.'
    (library/'README.md').write_text('# Thư viện style\n\n'+note+'\n\nDùng scripts/style_packages.py list hoặc mở index.html.\n',encoding='utf-8')
    items=''.join(f'<li><a href="{html.escape(p["id"])}/README.md">{html.escape(p["id"]+" — "+p["name"])}</a></li>' for p in catalog)
    (library/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Thư viện style</title><h1>Editing style packages</h1><p>'+note+'</p><ul>'+items+'</ul>',encoding='utf-8')
    # Development-only commands depend on private golden frames; never ship them.
    package_path=engine/'package.json'
    package=json.loads(package_path.read_text(encoding='utf-8'))
    for command in ['goldens','motion:prepare']:package['scripts'].pop(command,None)
    package_path.write_text(json.dumps(package,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for rel in (ROOT/PLUGIN).rglob('*'):
        if rel.is_file():
            target=dest/rel.relative_to(ROOT/PLUGIN);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(rel,target)
    (dest/'BAT-DAU.md').write_text('# Bắt đầu\n\nMở [trang hướng dẫn](engine/bat-dau.html) hoặc [BAT-DAU.md](engine/BAT-DAU.md). Bộ dựng nằm trong thư mục engine.\n',encoding='utf-8')
    for folder in ['out','public/raw']:(engine/folder).mkdir(parents=True,exist_ok=True)
    # No downloaded customer demo. This clip is generated from color + silence only.
    import subprocess
    sample=engine/'public/samples/setup-test.mp4';sample.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=0x253c33:s=960x540:r=30',
                    '-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-t','3','-c:v','libx264',
                    '-pix_fmt','yuv420p','-c:a','aac','-shortest',str(sample)],check=True)
    manifest=[]
    for path in sorted(dest.rglob('*')):
        if path.is_file():manifest.append({'path':path.relative_to(dest).as_posix(),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    (dest/'CONTENTS.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'PACK_FOLDER={dest}')
    if not a.no_zip:
        archive=release.parent/f'{release.name}.zip'
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
            for path in sorted(dest.rglob('*')):
                if path.is_file():z.write(path,path.relative_to(release))
        print(f'PACK_ZIP={archive}')
        print(f'FILES={len(manifest)+1}; SIZE_MB={archive.stat().st_size/1024/1024:.1f}')
    print('Đã đóng gói; chưa có nghĩa plugin đã được cài trong Work.')

if __name__=='__main__':
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8')
    main()
