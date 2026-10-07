"""Read-only, host-neutral prerequisites check. No downloads or installations."""
import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def version_of(cmd):
    executable=shutil.which(cmd[0])
    if not executable:return None
    try:
        r=subprocess.run([executable,*cmd[1:]],capture_output=True,text=True,timeout=20)
        lines=(r.stdout or r.stderr).strip().splitlines()
        return lines[0] if r.returncode==0 and lines else None
    except (OSError,subprocess.TimeoutExpired):return None

def collect(mode='all',root=ROOT):
    checks=[]
    def add(name,ok,detail,required=True):checks.append(dict(name=name,ok=bool(ok),required=required,detail=detail))
    add('python',sys.version_info>=(3,10),sys.version.split()[0])
    node=version_of(['node','--version'])
    major=node.lstrip('v').split('.')[0] if node else ''
    add('node',major.isdigit() and int(major)>=18,node or 'Cần Node.js 18 trở lên.')
    for executable in ('ffmpeg','ffprobe'):
        version=version_of([executable,'-version'])
        add(executable,version,version or f'Chưa tìm thấy {executable} trong PATH.')
    add('remotion',(root/'node_modules/remotion/package.json').is_file(),'Chạy npm ci trong thư mục bộ dựng nếu còn thiếu.')
    add('engine',(root/'src/Root.tsx').is_file() and (root/'scripts/render-edit.py').is_file(),'Mã dựng và công cụ xuất video.')
    for module in ('faster_whisper','cv2','numpy','PIL'):
        try:present=importlib.util.find_spec(module) is not None
        except (ImportError,ValueError):present=False
        add(module,present,'Cần cho nguồn mới; không bắt cài lại khi chỉ xuất EDL có sẵn.',required=mode=='all')
    render_ready=all(c['ok'] for c in checks if c['name'] not in ('faster_whisper','cv2','numpy','PIL'))
    transcribe_ready=all(c['ok'] for c in checks if c['name'] in ('python','ffmpeg','faster_whisper'))
    return {'engineRoot':str(root.resolve()),'mode':mode,'ready':all(c['ok'] for c in checks if c['required']),
            'renderDependenciesReady':render_ready,'transcribeDependenciesReady':transcribe_ready,'checks':checks,
            'notes':['Kiểm tra này không thay cho xuất thử một video.',
            'Lần đầu có thể cần mạng để tải mô hình giọng nói, font hoặc trình dựng.',
            'Luồng clean dùng AI đang trò chuyện; không yêu cầu Claude CLI hoặc API key.']}

def main():
    p=argparse.ArgumentParser(description='Kiểm tra công cụ dựng trên máy hiện tại.')
    p.add_argument('--mode',choices=['all','render'],default='all');p.add_argument('--json',action='store_true')
    a=p.parse_args();report=collect(a.mode)
    if a.json:print(json.dumps(report,ensure_ascii=False,indent=2))
    else:
        print(f'Kiểm tra bộ dựng tại {ROOT}')
        for c in report['checks']:
            label='OK' if c['ok'] else 'THIẾU' if c['required'] else 'TÙY CHỌN'
            print(f'[{label}] {c["name"]}: {c["detail"]}')
        print('Đủ công cụ để thử dựng.' if report['ready'] else 'Cần bổ sung các mục THIẾU trước khi dựng.')
        for note in report['notes']:print(note)
    return 0 if report['ready'] else 1
if __name__=='__main__':
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
