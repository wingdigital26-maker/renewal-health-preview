# -*- coding: utf-8 -*-
"""2026-07-23 redesign pass: floaters out, word band out, nav consolidation,
first-section-only reveal, layout variety, immersive over-hero header,
one-time home dragonfly entrance, Lynette two-column bio block.
Pure structure/markup. No visible copy is added, removed, or reworded."""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = [os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html"))
         if os.path.basename(p) != "cart.html"]

# hero variant + article variant assignment (distributed so consecutive pages differ
# and pages lead with different treatments)
HERO = {
  "naturopathic-detox.html": "",
  "services.html": "ph-left",
  "gut-health-support.html": "ph-quiet",
  "weight-metabolic-health.html": "ph-band",
  "hormone-balance-support.html": "",
  "inflammation-support.html": "ph-left",
  "emotional-overwhelm-nervous-system.html": "ph-quiet",
  "neurodivergent-support.html": "ph-band",
  "programs-packages.html": "ph-left",
  "about.html": "ph-quiet",
  "about-lynette-wing-renewal-health.html": "ph-quiet",
  "why-a-dragonfly-renewal-health.html": "ph-band",
  "naturopathy-homeopathy-holistic-healing.html": "",
  "testimonials.html": "ph-left",
  "blog.html": "ph-quiet",
  "contact-renewal-health.html": "",
  "resources.html": "ph-band",
}
ART = {
  "naturopathic-detox.html": "av-band",
  "services.html": "av-offset art-white",
  "gut-health-support.html": "av-panel",
  "weight-metabolic-health.html": "av-band art-white",
  "hormone-balance-support.html": "av-offset",
  "inflammation-support.html": "av-panel art-white",
  "emotional-overwhelm-nervous-system.html": "av-band",
  "neurodivergent-support.html": "av-offset art-white",
  "programs-packages.html": "av-panel",
  "about.html": "",
  "about-lynette-wing-renewal-health.html": "",
  "why-a-dragonfly-renewal-health.html": "av-band art-white",
  "naturopathy-homeopathy-holistic-healing.html": "av-offset",
  "testimonials.html": "av-panel art-white",
}

DF_SVG = re.compile(r'\s*<svg class="hero-dragonfly".*?</svg>', re.S)
WORD_BAND = re.compile(r'\s*<div class="word-band"[^>]*>.*?</div>\s*</div>', re.S)

NAV_DROP_OLD = '<li><a href="neurodivergent-support.html">Neurodivergent Support</a></li></ul></li>'
NAV_DROP_NEW = ('<li><a href="neurodivergent-support.html">Neurodivergent Support</a></li>'
                '<li class="drop-sep"><a href="programs-packages.html">Programs &amp; Packages</a></li></ul></li>')
NAV_STANDALONE = '\n        <li><a href="programs-packages.html">Programs &amp; Packages</a></li>'

# home hero entrance dragonfly (single, tasteful, flies bottom-left -> top-right)
DF_ENTRANCE = '''  <svg class="df-entrance" viewBox="0 0 100 100" fill="none" aria-hidden="true">
  <g stroke="currentColor" stroke-width="1.6" stroke-linecap="round">
    <ellipse cx="32" cy="38" rx="24" ry="9" transform="rotate(-24 32 38)" fill="currentColor" fill-opacity=".16"/>
    <ellipse cx="68" cy="38" rx="24" ry="9" transform="rotate(24 68 38)" fill="currentColor" fill-opacity=".16"/>
    <ellipse cx="34" cy="52" rx="20" ry="7.5" transform="rotate(-38 34 52)" fill="currentColor" fill-opacity=".12"/>
    <ellipse cx="66" cy="52" rx="20" ry="7.5" transform="rotate(38 66 52)" fill="currentColor" fill-opacity=".12"/>
    <circle cx="50" cy="30" r="4.5" fill="currentColor"/>
    <path d="M50 35 L50 88" stroke-width="3"/>
    <path d="M47 84 L50 92 L53 84" stroke-width="2"/>
  </g>
</svg>
'''

BIO = re.compile(
  r'<figure class="reveal">(<img src="[^"]*lynette-wing[^"]*"[^>]*>)</figure>\s*'
  r'(<h2 class="reveal">.*?</h2>)\s*(<p>.*?</p>)\s*(<p>.*?</p>)', re.S)

def transform(fn, src):
    # 1. remove ALL floating/decorative dragonflies
    src = DF_SVG.sub("", src)

    # 8. remove the scrolling word band (home/index only)
    src = WORD_BAND.sub("", src)

    # 3. consolidate nav: fold Programs & Packages into the Services dropdown,
    #    drop the standalone top-level item
    src = src.replace(NAV_DROP_OLD, NAV_DROP_NEW)
    src = src.replace(NAV_STANDALONE, "")

    # 7. immersive over-hero header
    src = src.replace('<body>', '<body class="has-hero">', 1)

    # 6. home hero entrance dragonfly (insert after the veil)
    if 'home-hero-veil' in src:
        src = src.replace('<div class="home-hero-veil"></div>\n',
                          '<div class="home-hero-veil"></div>\n' + DF_ENTRANCE, 1)

    # 9. Lynette portrait -> two-column bio block (content left, photo right)
    src = BIO.sub(
        r'<div class="bio-block"><div class="bio-copy">\2\n\3\n\4</div>'
        r'<div class="bio-portrait"><figure>\1</figure></div></div>', src)

    # 1. hero variant class
    hv = HERO.get(fn, "")
    if hv:
        src = src.replace('<section class="page-hero">',
                          '<section class="page-hero %s">' % hv, 1)

    # 1. article variant class
    av = ART.get(fn, "")
    if av:
        src = src.replace('<section class="section article">',
                          '<section class="section article %s">' % av, 1)

    # 2. first content section is the intro-reveal (the only animated section)
    src = re.sub(r'<section class="section ',
                 '<section class="section intro-reveal ', src, count=1)

    return src

for fn in PAGES:
    p = os.path.join(ROOT, fn)
    src = open(p, encoding="utf-8").read()
    new = transform(fn, src)
    if new != src:
        open(p, "w", encoding="utf-8").write(new)
        print("updated", fn)
    else:
        print("nochange", fn)
