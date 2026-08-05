"""Extract visible text per page for before/after content-preservation QA."""
import re, sys, json, os, glob, html

SKIP_DIRS = ('blog/category', 'blog/tag')

def visible(path):
    s = open(path, encoding='utf8').read()
    m = re.search(r'<main\b[^>]*>(.*?)</main>', s, re.S)
    body = m.group(1) if m else s
    body = re.sub(r'<(script|style|svg)\b.*?</\1>', ' ', body, flags=re.S | re.I)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = html.unescape(body)
    return re.findall(r"[\w’'%$&/.-]+", body)

def snap(out):
    files = sorted(glob.glob('*.html')) + sorted(glob.glob('blog/*.html'))
    data = {}
    for f in files:
        if f == 'cart.html':
            continue
        data[f] = visible(f)
    json.dump(data, open(out, 'w', encoding='utf8'))
    print('snapped', len(data), 'pages ->', out)

def diff(a, b):
    A = json.load(open(a, encoding='utf8'))
    B = json.load(open(b, encoding='utf8'))
    for k in sorted(set(A) | set(B)):
        wa, wb = A.get(k), B.get(k)
        if wa is None:
            print(f'{k}: NEW ({len(wb)} words)'); continue
        if wb is None:
            print(f'{k}: REMOVED'); continue
        if wa == wb:
            continue
        sa, sb = set(wa), set(wb)
        print(f'{k}: {len(wa)} -> {len(wb)} ({len(wb)-len(wa):+d} words)')
        gone = [w for w in wa if w not in sb]
        added = [w for w in wb if w not in sa]
        if gone:
            print('   words gone entirely:', gone[:40])
        if added:
            print('   words added:', added[:40])
        # sentence-level: what text blocks disappeared
        import difflib
        sm = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == 'equal':
                continue
            print(f'   [{tag}] -: {" ".join(wa[i1:i2])[:300]!r}')
            print(f'          +: {" ".join(wb[j1:j2])[:300]!r}')

if __name__ == '__main__':
    if sys.argv[1] == 'snap':
        snap(sys.argv[2])
    else:
        diff(sys.argv[2], sys.argv[3])
