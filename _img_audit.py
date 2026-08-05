import os, re, collections

root = os.path.abspath('.')
SEP = chr(92)

def norm(p):
    return p.replace(SEP, '/')

pages = []
for dp, dn, fn in os.walk(root):
    for f in fn:
        if f.endswith('.html'):
            pages.append(norm(os.path.relpath(os.path.join(dp, f), root)))

usage = collections.defaultdict(list)
pat = re.compile(r'''(?:src|href|srcset)\s*=\s*["']([^"']+\.(?:jpg|jpeg|png|webp|gif|svg|ico|avif))''', re.I)
pat2 = re.compile(r'''url\(\s*["']?([^"'\)]+\.(?:jpg|jpeg|png|webp|gif|svg|ico|avif))''', re.I)

for p in sorted(pages):
    if p.startswith('blog/category') or p.startswith('blog/tag') or p == 'cart.html':
        continue
    txt = open(os.path.join(root, p), encoding='utf-8', errors='replace').read()
    for m in list(pat.finditer(txt)) + list(pat2.finditer(txt)):
        u = m.group(1)
        if u.startswith('http') or u.startswith('data:') or u.startswith('//'):
            continue
        base = norm(os.path.normpath(os.path.join(os.path.dirname(p), u)))
        usage[base].append(p)

rows = [(k, sorted(set(v)), len(usage[k])) for k, v in sorted(usage.items())]
dupes = [(k, v, n) for k, v, n in rows if len(v) > 1]
print("distinct images referenced:", len(rows))
print("")
print("=== MULTI-PAGE (dupes) ===")
for k, v, n in dupes:
    print(k)
    for pg in v:
        print("    ", pg)
print("")
print("=== ALL (refcount, image, pages) ===")
for k, v, n in rows:
    print(n, k, v)
