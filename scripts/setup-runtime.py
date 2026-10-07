"""Install project dependencies only when --install is explicitly supplied."""
import argparse
import json
import shutil
import subprocess
import sys
import venv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(description='Chuẩn bị bộ dựng trong đúng thư mục này.')
    ap.add_argument('--install',action='store_true',help='Tạo môi trường Python riêng và cài phụ thuộc dự án; cần mạng.')
    ap.add_argument('--mode',choices=['all','render'],default='all');a=ap.parse_args()
    package=json.loads((ROOT/'package.json').read_text(encoding='utf-8'))
    if package['name']!='video-editor-kit' or not (ROOT/'src/Root.tsx').is_file():raise SystemExit('Đây không phải thư mục bộ dựng.')
    python=ROOT/('.venv/Scripts/python.exe' if sys.platform=='win32' else '.venv/bin/python')
    if a.install:
        npm=shutil.which('npm.cmd' if sys.platform=='win32' else 'npm')
        if not npm:raise SystemExit('Chưa có Node.js/npm. AI cần hướng dẫn cài đúng hệ điều hành trước.')
        if not python.exists():venv.EnvBuilder(with_pip=True).create(ROOT/'.venv')
        if not (ROOT/'node_modules/remotion/package.json').is_file():subprocess.run([npm,'ci'],cwd=ROOT,check=True)
        if a.mode=='all':
            check=subprocess.run([str(python),'-c','import faster_whisper, cv2, numpy, PIL'],capture_output=True)
            if check.returncode:
                subprocess.run([str(python),'-m','pip','install','-r',str(ROOT/'requirements.txt')],cwd=ROOT,check=True)
    subprocess.run([str(python) if python.exists() else sys.executable,str(ROOT/'scripts/doctor.py'),'--mode',a.mode,'--json'],cwd=ROOT,check=True)
if __name__=='__main__':
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8')
    main()
