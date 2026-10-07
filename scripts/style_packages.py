"""Deterministic editorial-contract checks. No aesthetic/semantic quality claim."""
import argparse, collections, hashlib, json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LIBRARY=ROOT/'asset-library/style-packages'
QUIET={'speaker','speaker-window','gentle-push','pullback','wide-reset','punch-cut','held-caption'}
ROLES={'hook','setup','explain','example','proof','contrast','takeaway','close','bridge'}
def load_package(package_id, library=LIBRARY):
    if not isinstance(package_id,str) or package_id not in {f'R{i:02}' for i in range(1,18)}|{f'S{i:02}' for i in range(1,5)}:
        raise ValueError('Unknown style package ID')
    return json.loads((library/package_id/'package.json').read_text(encoding='utf-8'))

def asset_identity(asset,public_dir):
    """Exact decoded-image/crop identity catches renames and lossless re-exports."""
    name=asset.get('file','')
    if not isinstance(name,str) or not name:raise ValueError('Asset needs a local file')
    path=(public_dir/name).resolve()
    if not path.is_relative_to(public_dir.resolve()) or not path.is_file():
        raise ValueError(f'Missing asset or outside public/: {name}')
    if asset.get('kind','image')=='image':
        from PIL import Image
        with Image.open(path) as src:
            im=src.convert('RGB')
            if asset.get('crop') is not None:
                crop=asset['crop']
                if not (isinstance(crop,list) and len(crop)==4 and all(isinstance(v,(float,int)) and not isinstance(v,bool) and math.isfinite(v) for v in crop)):
                    raise ValueError('crop must be normalized [x,y,w,h]')
                x,y,w,h=crop
                if not(0<=x<1 and 0<=y<1 and w>0 and h>0 and x+w<=1.000001 and y+h<=1.000001):raise ValueError('Invalid asset crop')
                box=(round(x*im.width),round(y*im.height),round((x+w)*im.width),round((y+h)*im.height))
                if box[2]<=box[0] or box[3]<=box[1]:raise ValueError('Empty asset crop')
                im=im.crop(box)
            return hashlib.sha256(str(im.size).encode()+im.tobytes()).hexdigest()
    if asset.get('crop') is not None:raise ValueError('Crop fingerprint is supported for image assets only')
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def validate_plan(plan,package=None,public_dir=ROOT/'public'):
    errors=[];warnings=[]
    def err(code,message,beat=None):errors.append(dict(code=code,message=message,**({'beat':beat} if beat else {})))
    if not isinstance(plan,dict):return {'ok':False,'errors':[{'code':'plan-shape','message':'Plan must be an object'}],'warnings':[]}
    try:package=package or load_package(plan.get('stylePackage'))
    except (ValueError,OSError,json.JSONDecodeError) as e:return {'ok':False,'errors':[{'code':'package','message':str(e)}],'warnings':[]}
    policy=package['policy']
    if plan.get('stylePackage')!=package['id'] or plan.get('packageVersion')!=package['version']:err('package-version','Package ID/version does not match the selected contract')
    if plan.get('status')!='reviewed':err('draft','Fill and review the form before rendering')
    if plan.get('timebase')!='edited-clip':err('timebase','Use edited-clip timebase after source cuts')
    duration=plan.get('durationMs')
    if not isinstance(duration,(int,float)) or isinstance(duration,bool) or not math.isfinite(duration) or duration<=0:
        err('duration','A finite positive durationMs is required');duration=1
    if plan.get('aspect') not in policy['supportedPlanAspects']:err('aspect','Aspect must be 9:16 or 16:9')
    if plan.get('aspect')=='16:9':warnings.append({'code':'landscape-adaptation','message':'Refs are portrait; landscape layout needs its own visual check'})
    clip=plan.get('clip')
    if not isinstance(clip,str) or not clip:err('clip','Set the actual source clip')
    else:
        path=(public_dir/clip).resolve()
        if not path.is_relative_to(public_dir.resolve()) or not path.is_file():err('clip-file','Source clip missing or outside public/')
    for field in ('audience','promise','takeaway'):
        if not str((plan.get('brief') or {}).get(field) or '').strip():err('brief',f'Brief needs {field}')
    assets=plan.get('assets',[]);registry={};fingerprints={}
    if not isinstance(assets,list):err('assets','Assets must be an array');assets=[]
    for a in assets:
        if not isinstance(a,dict) or not a.get('id'):err('asset-id','Each asset needs an ID');continue
        if a['id'] in registry:err('asset-id','Duplicate asset ID: '+a['id']);continue
        registry[a['id']]=a
        if not str(a.get('meaning') or '').strip():err('asset-meaning','Describe what the asset proves: '+a['id'])
        try:fingerprints[a['id']]=asset_identity(a,public_dir)
        except (OSError,ValueError,TypeError) as e:err('asset-file',str(e))
    beats=plan.get('beats',[])
    if not isinstance(beats,list) or not beats:err('beats','A reviewed beat sheet is required');beats=[]
    seen_ids=set();valid=[];last_end=0;usage=collections.defaultdict(list);graphic=[];run=0;last_graphic_end=None
    for b in beats:
        if not isinstance(b,dict):err('beat-shape','Beat must be an object');continue
        bid=b.get('id')
        if not isinstance(bid,str) or not bid or bid in seen_ids:err('beat-id','Beat IDs must be present and unique');continue
        seen_ids.add(bid)
        start,end=b.get('startMs'),b.get('endMs')
        numeric=all(isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) for v in (start,end))
        if not numeric or not(0<=start<end<=duration):err('beat-time','Invalid start/end or outside duration',bid);continue
        if start<last_end:err('beat-overlap','Beats must be chronological and non-overlapping',bid)
        last_end=end;valid.append(b)
        layout=b.get('layout')
        if layout not in policy['allowedLayouts']:err('layout','Layout is outside selected package: '+str(layout),bid)
        if b.get('package',package['id'])!=package['id']:err('style-mix','Do not mix packages without a new explicit project contract',bid)
        if b.get('role') not in ROLES:err('role','Set a valid narrative role',bid)
        if not str(b.get('meaning') or '').strip():err('meaning','Explain why this beat exists',bid)
        if not str(b.get('referenceEvent') or '').strip():err('reference-event','Link this choice to a source event or stated adaptation',bid)
        enter,leave=b.get('entryMs'),b.get('exitMs')
        if not all(isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) and v>=0 for v in (enter,leave)):
            err('motion-time','Entry and exit must be finite nonnegative durations',bid)
        elif enter+leave>end-start:err('motion-hold','Entry + exit exceed beat duration',bid)
        ids=b.get('assetIds',[])
        if not isinstance(ids,list) or any(not isinstance(x,str) for x in ids):err('asset-ids','assetIds must be a string array',bid);ids=[]
        if len(ids)!=len(set(ids)):err('asset-duplicate-in-beat','One asset appears twice in this composition',bid)
        if layout=='collage' and len(ids) not in (2,3):err('collage-size','A collage needs 2–3 distinct relevant assets',bid)
        if layout in ('numbered-image','product-callout') and len(ids)!=1:err('single-image','This layout needs exactly one object asset',bid)
        for aid in ids:
            if aid not in registry:err('asset-unknown','Unknown asset '+aid,bid);continue
            if aid not in fingerprints:continue
            identity=fingerprints[aid];previous=usage[identity]
            if previous:
                original=previous[0];callback=b.get('callbackOf')==original['id']
                reason=bool(str(b.get('callbackReason') or '').strip())
                same_concept=bool(b.get('conceptId')) and b.get('conceptId')==original.get('conceptId')
                gap=start-original['endMs']>=policy['callbackMinGapMs']
                if not(callback and reason and same_concept and gap and len(previous)==1):
                    err('asset-reuse',f'{aid} repeats picture content from {original["id"]}; use a new meaningful asset or keep the speaker',bid)
            previous.append(b)
        if layout not in QUIET:
            graphic.append(b)
            run=run+1 if last_graphic_end is not None and start-last_graphic_end<2000 else 1
            last_graphic_end=end
            if run>policy['maxConsecutiveGraphicBeats']:err('no-breathing-room',f'More than {policy["maxConsecutiveGraphicBeats"]} graphic beats without a two-second clean interval',bid)
    occupancy=sum(b['endMs']-b['startMs'] for b in graphic)/duration
    if occupancy>policy['maxGraphicOccupancy']+.00001:err('graphic-occupancy',f'Graphic occupancy {occupancy:.0%} exceeds package limit {policy["maxGraphicOccupancy"]:.0%}')
    # Sliding windows catch a burst hidden by averaging over a long quiet ending.
    for b in graphic:
        n=sum(b['startMs']<=x['startMs']<b['startMs']+60000 for x in graphic)
        if n>policy['maxGraphicBeatsPerMinute']:
            err('graphic-frequency',f'{n} graphic beats within 60s; limit {policy["maxGraphicBeatsPerMinute"]}',b['id']);break
    caps=plan.get('captions',[]);end=0
    if not isinstance(caps,list):err('caption-shape','Captions must be an array');caps=[]
    for c in caps:
        if not isinstance(c,dict):err('caption-shape','Caption must be an object');continue
        a,b=c.get('startMs'),c.get('endMs')
        if not all(isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) for v in (a,b)) or not (end<=a<b<=duration):err('caption-time','Caption overlaps or has invalid timing');continue
        end=b
        if not 1<=len(str(c.get('text') or '').split())<=policy['maxCaptionWords']:err('caption-length','Caption needs 1–5 words; preserve meaning instead of truncating')
    sfx=(plan.get('audio') or {}).get('sfx',[])
    if not isinstance(sfx,list):err('sfx-shape','SFX must be an array');sfx=[]
    times=[]
    for s in sfx:
        t=s.get('startMs') if isinstance(s,dict) else None
        if not isinstance(t,(int,float)) or isinstance(t,bool) or not math.isfinite(t) or not 0<=t<duration:err('sfx-time','Invalid SFX time')
        else:times.append(t)
    if any(sum(t<=x<t+60000 for x in times)>policy['maxSfxPerMinute'] for t in times):err('sfx-frequency','Too many SFX within 60 seconds')
    warnings.append({'code':'review-limit','message':'Checks catch structure/reuse/timing, not artistic quality or natural speech. Compare a short render with source evidence and listen to joins.'})
    return {'ok':not errors,'package':package['id'],'errors':errors,'warnings':warnings,
      'metrics':{'beats':len(valid),'graphicBeats':len(graphic),'graphicOccupancy':round(occupancy,4),'registeredAssets':len(registry),'uniqueImageContents':len(set(fingerprints.values())),'nestedModelCalls':0}}

def reject_unimplemented_package(plan):
    if plan.get('stylePackage'):
        raise ValueError('stylePackage is an editorial contract, not a clean/premium renderer alias. Use its beat sheet and an explicitly implemented, visually verified adapter; refusing silent generic rendering.')

def main():
    ap=argparse.ArgumentParser(description='Gói dựng từ ref: tạo form và kiểm tra kế hoạch, không gọi thêm AI.')
    sub=ap.add_subparsers(dest='command',required=True)
    sub.add_parser('list')
    new=sub.add_parser('new');new.add_argument('package');new.add_argument('--out',required=True)
    check=sub.add_parser('check');check.add_argument('plan');check.add_argument('--report');check.add_argument('--public-dir',default=str(ROOT/'public'))
    a=ap.parse_args()
    if a.command=='list':
        for p in json.loads((LIBRARY/'catalog.json').read_text(encoding='utf-8'))['packages']:print(p['id']+' — '+p['name'])
    elif a.command=='new':
        p=load_package(a.package);target=Path(a.out);target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('x',encoding='utf-8') as f:f.write((LIBRARY/p['id']/'form.json').read_text(encoding='utf-8'))
        print(str(target))
    else:
        report=validate_plan(json.loads(Path(a.plan).read_text(encoding='utf-8')),public_dir=Path(a.public_dir))
        if a.report:
            path=Path(a.report);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(0 if report['ok'] else 1)
if __name__=='__main__':main()
