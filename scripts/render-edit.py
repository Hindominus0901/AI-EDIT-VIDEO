"""Render an existing edit without STT, planning or changing its working EDL."""
import argparse
from pathlib import Path
from pipeline_common import render_final

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out-dir',default='out')
    parser.add_argument('--aspect',choices=['source','9:16','16:9','both'],default='source')
    parser.add_argument('--open',action='store_true')
    parser.add_argument('--preview-seconds',type=float,help='Xuất đoạn đầu để kiểm tra; không thay EDL hoặc chạy lại STT.')
    args=parser.parse_args()
    aspects=['9:16','16:9'] if args.aspect=='both' else [args.aspect]
    render_final(Path(args.out_dir),args.open,aspects=aspects,preview_seconds=args.preview_seconds)
