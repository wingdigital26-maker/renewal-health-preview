# -*- coding: utf-8 -*-
"""Source fresh, unique, free-to-use figure images from Pexels.

Every slot on the site that currently reuses an image gets its own photo.
Nothing is hotlinked: each file is downloaded to assets/figures/ and recorded
in assets/figures/_ledger.json (id, photographer, source URL, licence, alt).
Photo IDs are de-duplicated against the existing assets/heroes/ ledger and
against each other, so no photo can appear twice anywhere on the site.
"""
import io
import json
import os
import sys
import urllib.parse
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from PIL import Image

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
KEY = None
for line in open("C:/Users/wjack/ghl-cli/.env", encoding="utf-8"):
    if line.startswith("PEXELS_API_KEY"):
        KEY = line.split("=", 1)[1].strip()
assert KEY, "no PEXELS_API_KEY"

OUT = "assets/figures"
os.makedirs(OUT, exist_ok=True)
LEDGER = os.path.join(OUT, "_ledger.json")
ledger = json.load(open(LEDGER, encoding="utf-8")) if os.path.exists(LEDGER) else {}

used = set()
heroes = json.load(open("assets/heroes/_ledger.json", encoding="utf-8"))
for v in heroes.values():
    used.add(v["id"])
for v in ledger.values():
    used.add(v["id"])
# photos already on the site from other sources
used.update([18151389, 6900840, 36612667, 31755546, 35642508, 25527014, 37186494])

# slot name -> (search query, alt text)
SLOTS = [
    ("fig-home-leaf-light", "sunlight through fresh green leaves", "Morning light filtering through fresh green leaves"),
    ("fig-emotional-misty-lake", "calm misty lake at dawn", "Still water and soft mist at first light"),
    ("fig-emotional-reeds", "reeds by still water", "Slender reeds standing in quiet water"),
    ("fig-gut-fresh-herbs", "fresh green herbs flat lay", "Fresh green culinary herbs laid out on a pale surface"),
    ("fig-gut-seedling", "young seedling growing in soil", "A young seedling opening its first leaves in dark soil"),
    ("fig-hormone-wildflowers", "purple wildflowers in a meadow", "Purple wildflowers moving in a summer meadow"),
    ("fig-hormone-blossom", "soft pink blossom branch", "Soft pink blossom on a bare spring branch"),
    ("fig-inflammation-river-stones", "smooth river stones in clear water", "Smooth river stones resting under clear running water"),
    ("fig-inflammation-aloe", "aloe vera plant close up", "Close view of a fresh aloe vera plant"),
    ("fig-inflammation-moss-dew", "dew drops on green moss", "Dew beading on a cushion of green moss"),
    ("fig-detox-water-pour", "clear water pouring into a glass", "Clear water pouring gently into a glass"),
    ("fig-detox-infused-water", "lemon and mint infused water", "Water infused with lemon and fresh mint"),
    ("fig-naturopathy-mortar", "mortar and pestle with dried herbs", "A stone mortar and pestle with dried herbs"),
    ("fig-naturopathy-pressed-flowers", "pressed dried flowers on paper", "Pressed dried flowers arranged on pale paper"),
    ("fig-neuro-forest-path", "quiet forest path soft light", "A quiet path winding through a softly lit wood"),
    ("fig-neuro-balanced-stones", "balanced stacked stones", "Smooth stones balanced in a quiet stack"),
    ("fig-programs-journal", "journal notebook with plant on desk", "An open journal and a small green plant on a pale desk"),
    ("fig-weight-vegetables", "fresh vegetables in a basket", "Fresh whole vegetables gathered in a basket"),
    ("fig-weight-morning-walk", "path through a field at sunrise", "A walking path through an open field at sunrise"),
    ("fig-weight-hills-sunrise", "soft sunrise over rolling hills", "Soft sunrise light spreading over rolling hills"),
    ("fig-dragonfly-pond-reeds", "lily pond with reflections", "Reflections drifting across a still lily pond"),
    ("fig-resources-herbal-tea", "herbal tea cup with dried flowers", "A cup of herbal tea beside dried flowers"),
    ("fig-rootcause-wildflower-field", "wildflower field at golden hour", "A field of wildflowers in warm golden light"),
]


def api(url):
    req = urllib.request.Request(url, headers={"Authorization": KEY, "User-Agent": UA})
    return json.load(urllib.request.urlopen(req, timeout=60))


def grab(slot, query, alt):
    if slot in ledger and os.path.exists(os.path.join(OUT, slot + ".jpg")):
        print("skip (have)", slot)
        return
    for page in range(1, 6):
        q = urllib.parse.quote(query)
        data = api("https://api.pexels.com/v1/search?query=%s&per_page=20&page=%d"
                   "&orientation=landscape&size=large" % (q, page))
        for ph in data.get("photos", []):
            if ph["id"] in used:
                continue
            src = ph["src"]["large2x"]
            raw = urllib.request.urlopen(urllib.request.Request(src, headers={"User-Agent": UA}), timeout=90).read()
            im = Image.open(io.BytesIO(raw)).convert("RGB")
            im.thumbnail((1600, 1600), Image.LANCZOS)
            path = os.path.join(OUT, slot + ".jpg")
            im.save(path, "JPEG", quality=82, optimize=True, progressive=True)
            used.add(ph["id"])
            ledger[slot] = {
                "id": ph["id"],
                "photographer": ph["photographer"],
                "url": ph["url"],
                "alt": alt,
                "pexels_alt": ph.get("alt", ""),
                "query": query,
                "license": "Pexels License (free for commercial use, no attribution required)",
                "kb": os.path.getsize(path) // 1024,
            }
            json.dump(ledger, open(LEDGER, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
            print("ok", slot, ph["id"], ph["photographer"], ledger[slot]["kb"], "kB")
            return
    raise SystemExit("exhausted: " + slot)


for slot, query, alt in SLOTS:
    grab(slot, query, alt)
print("done,", len(ledger), "figures")
