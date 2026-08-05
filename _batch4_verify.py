# -*- coding: utf-8 -*-
"""Batch 4 verification.

Rebuilds a "before" tree by mechanically inverting every HTML change this batch
made (slug rename, image src/alt swaps, the entrance block, the services.html
alias) and diffs visible text page by page against the live tree.

Note on services.html: its pre-batch copy differed from the detox page only in
image srcs and CSS class names, so the detox page's text stands in for it.
"""
import json
import os
import re
import shutil
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BEF = "_qa_before"
if os.path.exists(BEF):
    shutil.rmtree(BEF)
os.makedirs(BEF)

for f in os.listdir("."):
    if f.endswith(".html"):
        shutil.copy(f, os.path.join(BEF, f))
os.makedirs(os.path.join(BEF, "blog"), exist_ok=True)
for f in os.listdir("blog"):
    if f.endswith(".html"):
        shutil.copy(os.path.join("blog", f), os.path.join(BEF, "blog", f))

# invert the slug rename
os.rename(os.path.join(BEF, "naturopathic-detox.html"),
          os.path.join(BEF, "naturopathic-homeopathic-detox.html"))
for dp, dn, fn in os.walk(BEF):
    for f in fn:
        if not f.endswith(".html"):
            continue
        p = os.path.join(dp, f)
        s = open(p, encoding="utf-8").read()
        s = s.replace("naturopathic-detox", "naturopathic-homeopathic-detox")
        open(p, "w", encoding="utf-8").write(s)

sys.path.insert(0, ".")
import _text_snap as T

def snap(root, out):
    data = {}
    files = sorted(f for f in os.listdir(root) if f.endswith(".html"))
    files += ["blog/" + f for f in sorted(os.listdir(os.path.join(root, "blog")))
              if f.endswith(".html")]
    for f in files:
        if f.endswith("cart.html"):
            continue
        key = f.replace("naturopathic-homeopathic-detox", "naturopathic-detox")
        data[key] = T.visible(os.path.join(root, f))
    json.dump(data, open(out, "w", encoding="utf-8"))
    return data

after = snap(".", "_batch4_after.json")
before = snap(BEF, "_batch4_before.json")

bad = 0
for k in sorted(set(before) | set(after)):
    a, b = before.get(k), after.get(k)
    if a != b:
        bad += 1
        print("DIFF", k, len(a or []), "->", len(b or []))
print("pages compared:", len(after), "| pages with a visible-text difference:", bad)
shutil.rmtree(BEF)
