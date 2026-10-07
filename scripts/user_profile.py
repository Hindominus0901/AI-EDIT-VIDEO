"""Per-channel preferences. Explicit updates only; one-off briefs never mutate profiles."""
import argparse
import copy
import json
import re
import sys
from pathlib import Path
DEFAULTS={'interfaceLanguage':'vi','aspect':'9:16','style':'studio','captionLanguage':'source',
          'music':'auto','sfx':'sparse','assetPolicy':'provided-and-licensed','priority':'quality',
          'audience':'','topic':'','targetDurationSec':None,'avoid':[]}
ENUMS={'interfaceLanguage':{'vi'},'aspect':{'9:16','16:9','both'},'style':{'clean','studio','paper','mono','editorial-c','iman','hormozi','martell'},
       'captionLanguage':{'source','vi','en'},'music':{'auto','none','provided'},'sfx':{'sparse','none'},
       'assetPolicy':{'provided-only','provided-and-licensed','generation-allowed'},'priority':{'quality','speed'}}

def validate(prefs):
    if not isinstance(prefs,dict):raise ValueError('Lựa chọn phải là một đối tượng JSON.')
    unknown=set(prefs)-set(DEFAULTS)
    if unknown:raise ValueError('Trường chưa hỗ trợ: '+', '.join(sorted(unknown)))
    for key,value in prefs.items():
        if key in ENUMS and (not isinstance(value,str) or value not in ENUMS[key]):raise ValueError(f'Giá trị {key} chưa hợp lệ: {value}')
        if key in ('audience','topic') and (not isinstance(value,str) or len(value)>500):raise ValueError(f'{key} phải là mô tả ngắn.')
        if key=='targetDurationSec' and value is not None and (isinstance(value,bool) or not isinstance(value,(int,float)) or not 5<=value<=7200):raise ValueError('Thời lượng phải từ 5 đến 7200 giây hoặc null.')
        if key=='avoid' and (not isinstance(value,list) or len(value)>30 or any(not isinstance(v,str) or len(v)>200 for v in value)):raise ValueError('avoid phải là danh sách ghi chú ngắn.')
    return prefs

def profile_path(workspace,channel):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,47}',channel):raise ValueError('Mã kênh dùng chữ thường, số và dấu gạch nối, tối đa 48 ký tự.')
    if channel in {'con','prn','aux','nul',*[f'com{i}' for i in range(1,10)],*[f'lpt{i}' for i in range(1,10)]}:raise ValueError('Mã kênh trùng tên dành riêng của hệ điều hành.')
    root=Path(workspace).resolve()
    base=(root/'.video-editor/profiles').resolve();dest=(base/f'{channel}.json').resolve()
    if not base.is_relative_to(root) or not dest.is_relative_to(base):raise ValueError('Hồ sơ phải nằm trong thư mục dự án.')
    return dest

def read_profile(workspace,channel):
    path=profile_path(workspace,channel)
    if not path.exists():return {'schemaVersion':1,'channel':channel,'preferences':{}}
    result=json.loads(path.read_text(encoding='utf-8-sig'))
    if result.get('schemaVersion')!=1 or result.get('channel')!=channel:raise ValueError('Hồ sơ sai phiên bản hoặc sai kênh.')
    validate(result['preferences']);return result

def resolve(profile,brief):
    validate(profile.get('preferences',{}));validate(brief)
    return copy.deepcopy({**DEFAULTS,**profile.get('preferences',{}),**brief})

def save_profile(workspace,channel,patch):
    validate(patch);profile=read_profile(workspace,channel);profile['preferences'].update(patch)
    path=profile_path(workspace,channel);path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_suffix('.tmp');temporary.write_text(json.dumps(profile,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temporary.replace(path)
    return profile

def main():
    ap=argparse.ArgumentParser(description='Lưu hoặc đọc gu riêng của từng kênh.')
    ap.add_argument('action',choices=['show','save','resolve'])
    ap.add_argument('--workspace',default=str(Path(__file__).resolve().parents[1]));ap.add_argument('--channel',default='mac-dinh')
    ap.add_argument('--input',help='File JSON gồm lựa chọn cần lưu hoặc ghi đè cho lượt này.')
    a=ap.parse_args();brief=json.loads(Path(a.input).read_text(encoding='utf-8-sig')) if a.input else {}
    if a.action=='save' and not a.input:ap.error('save cần --input; không lưu ngầm các giá trị mặc định.')
    profile=save_profile(a.workspace,a.channel,brief) if a.action=='save' else read_profile(a.workspace,a.channel)
    print(json.dumps(resolve(profile,brief) if a.action=='resolve' else profile,ensure_ascii=False,indent=2))
if __name__=='__main__':
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    main()
