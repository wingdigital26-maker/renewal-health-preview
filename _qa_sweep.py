"""Link/asset sweep + H1 count + title report across the rebuilt site."""
import os, re, glob, html
from urllib.parse import urlsplit, unquote

files = sorted(glob.glob('*.html')) + sorted(glob.glob('blog/**/*.html', recursive=True))
files = [f.replace('\\', '/') for f in files]

broken, checked, external = [], 0, set()
for f in files:
    s = open(f, encoding='utf8', errors='replace').read()
    base = os.path.dirname(f)
    for m in re.finditer(r'(?:href|src)\s*=\s*"([^"]+)"', s):
        ref = html.unescape(m.group(1)).strip()
        if not ref or ref.startswith(('#', 'data:', 'mailto:', 'tel:', 'javascript:')):
            continue
        u = urlsplit(ref)
        if u.scheme or u.netloc:
            external.add(u.netloc or ref[:40])
            continue
        p = unquote(u.path)
        if not p:
            continue
        target = os.path.normpath(os.path.join(base, p)) if not p.startswith('/') else p.lstrip('/')
        checked += 1
        if not os.path.exists(target):
            broken.append((f, ref))

print('local href/src references checked: %d across %d HTML files' % (checked, len(files)))
print('broken: %d' % len(broken))
for b in broken[:40]:
    print('   ', b)
print('external hosts referenced:', sorted(external))

print('\n-- H1 / title --')
bad = 0
for f in files:
    s = open(f, encoding='utf8', errors='replace').read()
    n = len(re.findall(r'<h1\b', s, re.I))
    t = re.search(r'<title>(.*?)</title>', s, re.S)
    if n != 1:
        bad += 1
        print('  !! %s has %d <h1>' % (f, n))
print('pages with exactly one H1: %d of %d (%d exceptions)' % (len(files) - bad, len(files), bad))
