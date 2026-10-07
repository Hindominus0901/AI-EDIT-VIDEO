"""Conservative timing planner. Transcript gaps are NOT proof of silence.

Long gaps are candidates; only gaps covered by an acoustic silence interval
can be shortened automatically. Emotional/protected spans always win.
Fillers/repetitions are review markers, never automatic deletions.
"""
import re


def plan_pacing(words, duration_ms, silences=(), protected=(), max_gap_ms=900,
                breath_ms=320, sentence_ms=600):
    if duration_ms <= 0 or max_gap_ms < 0 or breath_ms < 0 or sentence_ms < 0:
        raise ValueError('Invalid timing parameters')
    previous = -1
    for word in words:
        s, e = word['startMs'], word['endMs']
        if not 0 <= s <= e <= duration_ms or s < previous:
            raise ValueError('Words must be ordered and inside the source')
        previous = s
    removed, review = [], []
    for i, word in enumerate(words):
        normalized = word['text'].lower().strip(' .,?!:;')
        if normalized in {'um', 'uh', 'ừm', 'ờ', 'ờm'}:
            review.append({'kind': 'hesitation', 'startMs': word['startMs'],
                           'endMs': word['endMs'], 'action': 'keep-review-in-context'})
        if i and normalized == words[i-1]['text'].lower().strip(' .,?!:;'):
            review.append({'kind': 'repeat', 'startMs': words[i-1]['startMs'],
                           'endMs': word['endMs'], 'action': 'keep-may-be-emphasis'})
        if not i:
            continue
        a, b = words[i-1]['endMs'], word['startMs']
        if b-a <= max_gap_ms:
            continue
        if any(s < b and e > a for s, e in protected):
            review.append({'kind': 'protected-pause', 'startMs': a, 'endMs': b, 'action': 'keep'})
            continue
        # Retain more space after a sentence. Use only the acoustically silent
        # portion, preserving at least 80 ms next to each recognized word.
        retain = sentence_ms if re.search(r'[.!?…]["\u201d]*$', words[i-1]['text']) else breath_ms
        candidates = [(max(a+80, s), min(b-80, e)) for s, e in silences]
        candidates = [(s, e) for s, e in candidates if e-s > max(max_gap_ms, retain)]
        if not candidates:
            review.append({'kind': 'unverified-gap', 'startMs': a, 'endMs': b, 'action': 'keep'})
            continue
        s, e = max(candidates, key=lambda p:p[1]-p[0])
        cut_s, cut_e = s+retain/2, e-retain/2
        removed.append({'startMs': cut_s, 'endMs': cut_e,
                        'reason': 'verified-silence', 'retainedMs': b-a-(cut_e-cut_s)})
    spans, cursor = [], 0
    for cut in removed:
        if cut['startMs'] > cursor:
            spans.append([cursor, cut['startMs']])
        cursor = cut['endMs']
    if cursor < duration_ms:
        spans.append([cursor, duration_ms])
    return {'spans': spans, 'cuts': removed, 'review': review,
            'sourceDurationMs': duration_ms,
            'durationMs': sum(e-s for s,e in spans)}


def remap(words, spans):
    result, offset, wi = [], 0, 0
    for s,e in spans:
        while wi < len(words) and words[wi]['startMs'] < e:
            w = words[wi]
            if w['startMs'] >= s and w['endMs'] <= e:
                result.append({**w, 'startMs': round(offset+w['startMs']-s, 3),
                               'endMs': round(offset+w['endMs']-s, 3)})
            wi += 1
        offset += e-s
    return result
