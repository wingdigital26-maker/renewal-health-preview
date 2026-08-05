"""Merge the run of single-chunk `.section .inner.narrow.flow` bands on interior pages
into ONE continuous editorial article section. Pure structural merge: the inner content
of every merged section is preserved verbatim, in order. No text is added or removed."""
import os, re

ROOT = r"C:\Users\wjack\seo-factory\renewal-health\site-v2"

SEAM = re.compile(
    r'</div></section>\s*<section class="section bg-\w+"><div class="inner narrow flow">')
FIRST = re.compile(r'<section class="section bg-\w+"><div class="inner narrow flow">')

for fn in sorted(os.listdir(ROOT)):
    if not fn.endswith(".html") or fn in ("cart.html", "index.html", "home.html"):
        continue
    p = os.path.join(ROOT, fn)
    src = open(p, encoding="utf-8").read()
    merged, n = SEAM.subn("\n", src)
    if n == 0:
        print("%-52s no flow run" % fn)
        continue
    merged, n2 = FIRST.subn(
        '<section class="section article"><div class="inner narrow flow">', merged, count=1)
    open(p, "w", encoding="utf-8").write(merged)
    print("%-52s merged %d seams" % (fn, n))
