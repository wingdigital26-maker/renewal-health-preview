# -*- coding: utf-8 -*-
"""Replace every duplicated image reference so each photo appears exactly once.

Each entry is (page, old filename, occurrence index, new relative path, new alt).
Only the src and alt attributes change; no copy, markup or layout is touched.
"""
import io
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

FIG = "assets/figures/"
led = json.load(open(FIG + "_ledger.json", encoding="utf-8"))

# a few alts refined after eyeballing the downloads
led["fig-weight-hills-sunrise"]["alt"] = "Soft sunrise light spreading through low cloud"
led["fig-rootcause-wildflower-field"]["alt"] = "Seedheads catching warm golden light in an open field"
led["fig-inflammation-river-stones"]["alt"] = "Smooth river stones worn round by water"
json.dump(led, open(FIG + "_ledger.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)

INTER = "interconnected-holistic-health.jpg"
UNS = "unsplash-image-XDoGdUtTm-U.jpg"
RHNH = "renewal-health-naturopathy-homeopathy-1.jpg"

# page, old basename, occurrence (0-based), new slot (or explicit path), alt override
JOBS = [
    ("index.html", INTER, 0, "fig-home-leaf-light", None),
    ("home.html", INTER, 0, "fig-home-leaf-light", None),

    ("emotional-overwhelm-nervous-system.html", INTER, 0, "fig-emotional-misty-lake", None),
    ("emotional-overwhelm-nervous-system.html", "hero-dragonfly-lake.jpg", 0, "fig-emotional-reeds", None),

    ("gut-health-support.html", INTER, 0, "fig-gut-fresh-herbs", None),
    ("gut-health-support.html", "hero-programs-tea-pour.jpg", 0, "fig-gut-seedling", None),

    ("hormone-balance-support.html", INTER, 0, "fig-hormone-wildflowers", None),
    ("hormone-balance-support.html", "hero-contact-chamomile.jpg", 0, "fig-hormone-blossom", None),

    ("inflammation-support.html", INTER, 0, "fig-inflammation-river-stones", None),
    ("inflammation-support.html", UNS, 0, "fig-inflammation-aloe", None),
    ("inflammation-support.html", "hero-neuro-green-foliage.jpg", 0, "fig-inflammation-moss-dew", None),

    ("naturopathic-detox.html", INTER, 0, "fig-detox-water-pour", None),
    ("naturopathic-detox.html", UNS, 0, "fig-detox-infused-water", None),
    # the eucalyptus photo is freed up by the services.html alias, so it is
    # reused here as its one and only home on the site
    ("naturopathic-detox.html", "hero-gut-green-fern.jpg", 0,
     "assets/heroes/hero-services-eucalyptus.jpg", "Round eucalyptus stems in a glass vase"),

    ("naturopathy-homeopathy-holistic-healing.html", INTER, 0, "fig-naturopathy-mortar", None),
    ("naturopathy-homeopathy-holistic-healing.html", "hero-detox-herbal-botanical.jpg", 0,
     "fig-naturopathy-pressed-flowers", None),

    ("neurodivergent-support.html", INTER, 0, "fig-neuro-forest-path", None),
    ("neurodivergent-support.html", "hero-weight-succulents.jpg", 0, "fig-neuro-balanced-stones", None),

    ("programs-packages.html", INTER, 0, "fig-programs-journal", None),

    ("weight-metabolic-health.html", INTER, 0, "fig-weight-vegetables", None),
    ("weight-metabolic-health.html", UNS, 0, "fig-weight-morning-walk", None),
    ("weight-metabolic-health.html", "hero-naturopathy-dried-herbs.jpg", 0,
     "fig-weight-hills-sunrise", None),

    ("why-a-dragonfly-renewal-health.html", "hero-emotional-calm-water.jpg", 0,
     "fig-dragonfly-pond-reeds", None),

    ("resources.html", RHNH, 0, "fig-resources-herbal-tea", None),
    # the post keeps this photo as its hero (occurrence 0); the in-body repeat goes
    ("blog/root-cause-healing-naturopathy-homeopathy.html", RHNH, 1,
     "fig-rootcause-wildflower-field", None),

    # the surviving copy of the old unsplash photo gets meaningful alt text
    ("gut-health-support.html", UNS, 0, None, "Soft natural light across a calm still-life"),
]

IMG = re.compile(r'<img\b[^>]*>', re.I)


def apply(page, old, idx, slot, alt):
    txt = open(page, encoding="utf-8").read()
    prefix = "../" if "/" in page else ""
    hits = []
    for m in IMG.finditer(txt):
        s = re.search(r'src="([^"]*)"', m.group(0))
        if s and old in s.group(1):
            hits.append(m)
    if len(hits) <= idx:
        print("  MISS", page, old, idx)
        return False
    m = hits[idx]
    tag = m.group(0)
    new = tag
    if slot:
        path = slot if slot.startswith("assets/") else FIG + slot + ".jpg"
        assert os.path.exists(path), path
        new = re.sub(r'src="[^"]*"', 'src="' + prefix + path + '"', new)
    newalt = alt or (led[slot]["alt"] if slot and not slot.startswith("assets/") else alt)
    if newalt:
        if 'alt="' in new:
            new = re.sub(r'alt="[^"]*"', 'alt="' + newalt + '"', new)
        else:
            new = new[:-1].rstrip() + ' alt="' + newalt + '">'
    txt = txt[:m.start()] + new + txt[m.end():]
    open(page, "w", encoding="utf-8").write(txt)
    return True


n = 0
for page, old, idx, slot, alt in JOBS:
    if apply(page, old, idx, slot, alt):
        n += 1
print("applied", n, "of", len(JOBS))

# services.html is the same page as the detox page under a second URL; make it a
# true alias so the pair cannot introduce duplicate imagery.
src = open("naturopathic-detox.html", encoding="utf-8").read()
open("services.html", "w", encoding="utf-8").write(src)
print("services.html aliased to the detox page")
