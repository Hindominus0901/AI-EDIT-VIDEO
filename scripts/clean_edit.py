"""Approved clean edit policy. Local, deterministic, no nested LLM calls.

The host may provide edited-clip captions and semantic moments. Without them,
word timestamps are grouped conservatively and a small vocabulary suggests
highlights. The fallback is not a claim to understand the whole story.
"""
import copy
import json
import math
import re
from clean_media import media_tracks
import subprocess
from pathlib import Path

ACCENT = '#F3CE83'
PREMIUM_SETS = json.loads((Path(__file__).resolve().parents[1]/'src/premium-kit/sets.json').read_text(encoding='utf-8'))
PURE_SYSTEM = json.loads((Path(__file__).resolve().parents[1]/'src/pure-edit-system.json').read_text(encoding='utf-8'))
TERMS = {
    'thương hiệu': None, 'cá nhân': None, 'lợi thế': 'target',
    'bằng chứng': 'proof', 'uy tín': 'proof', 'ngách nhỏ': 'target',
    'trực tiếp': 'chat', 'phản hồi': 'chat', 'thời gian': 'time',
    'ý tưởng': 'idea', 'mục tiêu': 'target', 'tiến bộ': 'growth',
    'advantage': 'target', 'proof': 'proof', 'feedback': 'chat',
    'reputation': 'proof', 'time': 'time', 'idea': 'idea',
}
PAIRS = set(TERMS) | {'kỹ năng', 'chuyên môn', 'bắt đầu', 'nội dung', 'kinh doanh'}


def norm(text):
    return re.sub(r'[^\w\s]', '', text.lower()).strip()


def build_clean_captions(words):
    """Partition word timestamps into <=5 words, without dropping spoken words.

    A short dynamic program prefers 4-5 words and sentence/pause boundaries,
    and penalizes splitting known Vietnamese phrases. It never invents timing.
    """
    if not words:
        return []
    n = len(words)
    costs, ends = [math.inf] * (n+1), [0] * n
    costs[n] = 0
    for i in range(n-1, -1, -1):
        count = 0
        for j in range(i+1, min(n, i+5)+1):
            count += len(words[j-1]['text'].split())
            if count > 5:
                break
            length_cost = {1:16, 2:8, 3:3, 4:0, 5:0}[count]
            pause = j == n or words[j]['startMs'] - words[j-1]['endMs'] >= 320
            punctuation = words[j-1]['text'].rstrip().endswith(('.', '?', '!', ',', ':', ';'))
            splits_pair = j < n and (norm(words[j-1]['text'])+' '+norm(words[j]['text'])) in PAIRS
            # A phrase may not span a long pause just to hit a word count.
            internal_pause = any(words[k]['startMs']-words[k-1]['endMs'] >= 650 for k in range(i+1,j))
            score = costs[j] + 6 + length_cost - (3 if pause or punctuation else 0) + (12 if splits_pair else 0) + (24 if internal_pause else 0)
            if score < costs[i]:
                costs[i], ends[i] = score, j
    if not math.isfinite(costs[0]):
        raise ValueError('A transcript token exceeds five words; provide reviewed caption cues.')
    result, i = [], 0
    while i < n:
        j = ends[i]
        group = words[i:j]
        result.append({'text':' '.join(w['text'].strip() for w in group),
                       'startMs':group[0]['startMs'], 'endMs':group[-1]['endMs']})
        i = j
    for i,c in enumerate(result):
        if i+1 < len(result):
            next_start = result[i+1]['startMs']
            if 0 <= next_start-c['endMs'] <= 160:
                c['endMs'] = next_start  # avoid a one-frame flash between phrases
            c['endMs'] = min(c['endMs'], next_start)
    return result


def validate_captions(captions, duration_ms):
    last_end = 0
    for i,c in enumerate(captions):
        if not c.get('text','').strip() or len(c['text'].split()) > 5:
            raise ValueError(f'Caption {i}: needs 1-5 words; review text rather than truncate it.')
        if not (0 <= c['startMs'] < c['endMs'] <= duration_ms+1) or c['startMs'] < last_end:
            raise ValueError(f'Caption {i}: invalid, overlapping or out-of-range timing.')
        last_end = c['endMs']


def checked_asset(public_dir, name):
    path = (public_dir/name).resolve()
    if not path.is_relative_to(public_dir.resolve()) or not path.is_file():
        raise ValueError(f'Missing local asset or path outside public/: {name}')
    return name


def compose_clean(transcript, plan, clip, public_dir, aspect='source'):
    if 'creatorStyle' in plan:
        from creator_director import compose_creator
        return compose_creator(transcript, plan, clip, public_dir, aspect)
    from style_packages import reject_unimplemented_package
    reject_unimplemented_package(plan)
    pure_edit = bool(plan.get('pureEdit', False))
    look = plan.get('look')
    if look is not None and look not in PURE_SYSTEM['looks']:
        raise ValueError(f'Unknown pure-edit look: {look}')
    premium_set = plan.get('premiumSet')
    if pure_edit and premium_set is None:
        premium_set = PURE_SYSTEM['looks'].get(look, PURE_SYSTEM['defaultLook'])
    if premium_set is not None and premium_set not in PREMIUM_SETS:
        raise ValueError(f'Unknown premiumSet: {premium_set}')
    premium = PREMIUM_SETS.get(premium_set)
    duration = float(transcript['durationSec'])
    duration_ms = round(duration*1000)
    if plan.get('clip') and plan['clip'] != clip:
        raise ValueError('Host plan belongs to another clip.')
    if (plan.get('captions') is not None or plan.get('moments')) and plan.get('timebase') != 'edited-clip':
        raise ValueError('Timed host plans require timebase=edited-clip, after all source cuts.')
    if plan.get('captions') is not None:
        captions = copy.deepcopy(plan['captions'])
    else:
        captions = build_clean_captions(transcript['words'])
    validate_captions(captions, duration_ms)
    for i,c in enumerate(captions):
        continuous=i>0 and 0<=c['startMs']-captions[i-1]['endMs']<=160
        if continuous:captions[i-1]['endMs']=c['startMs']
        c['motion'] = {'entry':'hold' if continuous else 'rise'}
    if captions and captions[0]['endMs']-captions[0]['startMs'] >= 750:
        captions[0]['motion']['entry'] = 'word-rise'

    moments = plan.get('moments')
    mode = 'host semantic plan' if moments is not None else 'local vocabulary fallback'
    if moments is None:
        moments = []
        seen = set()
        for c in captions:
            for term,asset in TERMS.items():
                if f' {term} ' in f' {norm(c["text"])} ' and term not in seen:
                    moments.append({'sec':c['startMs']/1000,'keyword':term,'role':'emphasis',
                                    'asset':asset,'reason':'Local vocabulary match; conservative suggestion.'})
                    seen.add(term)
                    break
    graphics, sounds, decisions = [], [], []
    motion_rules = PURE_SYSTEM['motion']
    last_highlight, last_graphic, last_strong = -99999, -99999, -99999
    roles = {'hook':'word-rise', 'shift':'mask-up', 'proof':'rise',
             'example':'rise', 'emphasis':'soft-pop', 'close':'soft-pop'}
    asset_ids = json.loads((Path(__file__).resolve().parents[1]/'src/motion-kit/assets.json').read_text(encoding='utf-8'))
    for moment in sorted(moments,key=lambda m:m['sec']):
        keyword = str(moment.get('keyword','')).strip()
        when = float(moment['sec'])*1000
        matches = [c for c in captions if keyword and keyword.lower() in c['text'].lower()
                   and c['startMs']-750 <= when <= c['endMs']+750]
        if not matches:
            decisions.append({'keyword':keyword,'action':'skip','reason':'No matching caption near the stated time.'})
            continue
        c = min(matches,key=lambda x:abs(x['startMs']-when))
        start = c['startMs']
        if start-last_highlight < motion_rules['highlightGapMs']:
            decisions.append({'keyword':keyword,'action':'skip','reason':'Leave reading space after the preceding highlight.'})
            continue
        last_highlight = start
        role = moment.get('role','emphasis')
        if role not in roles:
            raise ValueError(f'Unknown moment role: {role}')
        strong = role in ('emphasis','close') and start-last_strong >= motion_rules['strongGapMs']
        if strong:
            last_strong = start
        entry = roles[role]
        if entry == 'soft-pop' and not strong:
            entry = 'rise'
        if c['endMs']-start < 700:
            entry = 'rise'
        c['motion'] = {'entry':entry,'keyword':keyword,'mark':'underline' if strong else 'color','strong':strong}
        if role == 'proof':
            c['motion']['mark'] = 'marker'
        decisions.append({'startMs':start,'keyword':keyword,'role':role,'entry':entry,
                          'reason':moment.get('reason','Semantic moment supplied by host.')})
        images = moment.get('images',[])
        asset = moment.get('asset')
        kind = moment.get('graphic','photo-window' if images else 'icon')
        if not asset and not images and not kind.startswith('ui-'):
            continue
        if start < motion_rules['openingClearMs'] or start-last_graphic < motion_rules['graphicGapMs']:
            decisions[-1]['graphic'] = 'omitted to keep opening/spacing clear'
            continue
        if kind not in ('photo-window','photo-circle','photo-collage','photo-mat','photo-diptych','photo-detail','icon','steps','ui-grid','ui-glass','ui-notification'):
            raise ValueError(f'Automatic layout requires a meaningful image/icon, got: {kind}')
        if asset and asset not in asset_ids:
            raise ValueError(f'Unknown vector asset: {asset}')
        needed = 2 if kind in ('photo-collage','photo-diptych') else 1 if kind.startswith('photo-') else 0
        if len(images) < needed:
            raise ValueError(f'{kind} requires {needed} local images.')
        for img in images:
            checked_asset(public_dir,img)
        # End with the supporting phrase unless the host explicitly supplies a
        # longer semantic window. A fixed hold can leak into the opposite idea.
        semantic_end = round(float(moment['endSec'])*1000) if 'endSec' in moment else c['endMs']
        if semantic_end <= start:
            raise ValueError(f'Graphic window for {keyword} ends before it starts.')
        end = min(duration_ms,start+motion_rules['graphicMaxMs'],semantic_end)
        if end-start < motion_rules['graphicMinMs']:
            continue
        motion = {'kind':kind}
        if asset: motion['asset'] = asset
        if images: motion['images'] = images
        if kind.startswith('ui-'): motion['text'] = str(moment.get('label') or keyword)[:80]
        graphics.append({'type':'clean-motion','startMs':start,'endMs':end,'motion':motion})
        last_graphic = start
        decisions[-1]['graphic'] = motion
        if moment.get('sound',False):
            sounds.append({'startMs':start+70,'sound':'kit-drop' if images else 'kit-tick',
                           'volume':.045 if images else .04,'preRollMs':0,'priority':5})

    info = json.loads(subprocess.run(['ffprobe','-v','error','-select_streams','v:0',
                     '-show_entries','stream=width,height','-of','json',str(public_dir/clip)],
                    check=True,capture_output=True,text=True).stdout)['streams'][0]
    portrait = aspect == '9:16' or (aspect == 'source' and info['height'] > info['width'])
    # Pure talking-head edits stay full-bleed. The focused preview layout
    # intentionally reserves a large caption canvas, which makes portrait
    # footage look like a small video sitting inside a black frame.
    layout = 'standard' if pure_edit else 'focused'
    edl = {'source':{'clip':clip,'durationSec':duration,'width':info['width'],'height':info['height'],'volume':1},
           'format':{'w':1080 if portrait else 1920,'h':1920 if portrait else 1080,'fps':30},
           'style':{'layout':layout,'ambient':'none','accent':ACCENT,'accent2':ACCENT,
                    'recipe':{'accent':ACCENT,'accent2':ACCENT,'highlightColor':ACCENT,'captionColor':'#FFFFFF',
                              'captionCase':'sentence','textFx':'solid','captionStrokePx':0,'scrimAlpha':0}},
           'tracks':{'captions':captions,'graphics':graphics,'sfx':sounds,'broll':[],'effects':[],'transitions':[]}}
    if premium:
        edl['style']['premiumSet'] = premium_set
        for c in captions:
            if c['motion']['entry']!='hold':
                c['motion']['entry'] = 'quiet-reveal' if c['motion']['entry'] == 'mask-up' else premium['entry']
            c['motion']['mark'] = 'underline' if c['motion'].get('strong') else 'color'
        edl['style']['accent'] = edl['style']['accent2'] = premium['accent']
        edl['style']['recipe'].update(accent=premium['accent'],accent2=premium['accent'],highlightColor=premium['accent'],captionColor=premium['foreground'])
    effects,broll=media_tracks(plan,duration_ms,public_dir,checked_asset)
    for g in graphics:
        if any(g['startMs']<b['endMs'] and g['endMs']>b['startMs'] for b in broll):
            raise ValueError('Supporting graphic overlaps B-roll; keep one visual emphasis at a time')
    edl['tracks']['effects']=effects
    edl['tracks']['broll']=broll
    if plan.get('music'):
        checked_asset(public_dir,plan['music']['src'])
        edl['music'] = {**plan['music'],'clipVolume':1}
    report = {'policy':'clean-v3','mode':mode,'decisions':decisions,'captions':len(captions),'cameraCues':len(effects),'brollClips':len(broll),
              'graphics':len(graphics),'sfx':len(sounds),'nestedModelCalls':0,
              'readingWarnings':[{'startMs':c['startMs'],'text':c['text']} for c in captions
                                 if (c['endMs']-c['startMs'])<650 or len(c['text'])/((c['endMs']-c['startMs'])/1000)>24]}
    if premium:
        report['premiumSet'] = premium_set
        for decision in report['decisions']:
            if 'startMs' in decision:
                decision['entry'] = next(c['motion']['entry'] for c in captions if c['startMs']==decision['startMs'])
    if pure_edit:
        report['pureEdit'] = {'systemVersion':PURE_SYSTEM['version'],'look':look or 'quiet',
                              'runtimeReferenceReads':0,'hostPlanFields':['pureEdit','look','moments']}
    return edl,report


def write_srt(path, captions):
    def stamp(ms):
        ms=round(ms)
        return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
    path.write_text('\n\n'.join(f'{i+1}\n{stamp(c["startMs"])} --> {stamp(c["endMs"])}\n{c["text"]}' for i,c in enumerate(captions))+'\n',encoding='utf-8')
