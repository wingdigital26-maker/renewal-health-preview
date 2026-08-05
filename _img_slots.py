import os, re, glob

files = sorted(glob.glob('*.html')) + sorted(glob.glob('blog/*.html'))
skip = {'cart.html', 'home.html', 'about-lynette-wing-renewal-health.html'}
for f in files:
    f = f.replace(chr(92), '/')
    if f in skip or f.startswith('blog/category') or f.startswith('blog/tag'):
        continue
    t = open(f, encoding='utf-8', errors='replace').read()
    print('##', f)
    for m in re.finditer(r'<img[^>]*>', t):
        tag = m.group(0)
        src = re.search(r'src="([^"]*)"', tag)
        alt = re.search(r'alt="([^"]*)"', tag)
        s = src.group(1) if src else '?'
        if 'renewalhealth2stack' in s:
            continue
        print('   ', os.path.basename(s), '| alt=', (alt.group(1) if alt else 'NONE'))
