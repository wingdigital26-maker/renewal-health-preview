# -*- coding: utf-8 -*-
"""Build real blog post pages from the ready drafts, plus the blog index.
Post wording is NOT altered: only the shell, image paths, and internal link
targets are adapted for the local static site."""
import re, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DRAFTS = os.path.join(ROOT, "..", "content", "drafts")

NAV = """<header class="v2-header">
  <div class="bar">
    <a class="v2-logo" href="{p}index.html"><img src="{p}assets/images.squarespace-cdn.com/content/v1/69de66d56f606e4d8a63fcb5/1557bced-4e06-4bfe-9242-8937f45cbe3d/renewalhealth2stack.jpg" alt="Renewal Health with Lynette Wing"></a>
    <nav class="v2-nav" aria-label="Main navigation">
      <ul>
        <li><a href="{p}index.html">Home</a></li>
        <li class="has-drop"><a href="{p}services.html">Services</a>
          <ul class="dropdown"><li><a href="{p}services.html">Services Overview</a></li><li><a href="{p}naturopathic-detox.html">Detox</a></li><li><a href="{p}gut-health-support.html">Gut Health Support</a></li><li><a href="{p}weight-metabolic-health.html">Weight Loss &amp; Metabolic Health</a></li><li><a href="{p}hormone-balance-support.html">Hormone Balance</a></li><li><a href="{p}inflammation-support.html">Inflammation Support</a></li><li><a href="{p}emotional-overwhelm-nervous-system.html">Emotional Overwhelm &amp; Nervous System Support</a></li><li><a href="{p}neurodivergent-support.html">Neurodivergent Support</a></li><li class="drop-sep"><a href="{p}programs-packages.html">Programs &amp; Packages</a></li></ul></li>
        <li class="has-drop"><a href="{p}about-lynette-wing-renewal-health.html">About</a>
          <ul class="dropdown"><li><a href="{p}about-lynette-wing-renewal-health.html">Meet Lynette Wing</a></li><li><a href="{p}why-a-dragonfly-renewal-health.html">Why a Dragonfly?</a></li><li><a href="{p}naturopathy-homeopathy-holistic-healing.html">What is Naturopathy and Homeopathy?</a></li></ul></li>
        <li><a href="{p}testimonials.html">Testimonials</a></li>
        <li><a href="{p}blog.html">Blog</a></li>
      </ul>
      <a class="btn btn-primary nav-cta" href="{p}contact-renewal-health.html">Contact</a>
    </nav>
    <button class="nav-toggle" aria-label="Menu"><span></span><span></span><span></span></button>
  </div>
</header>"""

FOOTER = """<footer class="v2-footer">
  <div class="inner">
    <div class="foot-grid">
      <div>
        <span class="foot-logo"><img src="{p}assets/images.squarespace-cdn.com/content/v1/69de66d56f606e4d8a63fcb5/1557bced-4e06-4bfe-9242-8937f45cbe3d/renewalhealth2stack.jpg" alt="Renewal Health with Lynette Wing"></span>
        <p class="foot-tag">Emerge. Align. Live Fully.</p>
      </div>
      <div><h5>Services</h5><ul><li><a href="{p}naturopathic-detox.html">Detox</a></li><li><a href="{p}gut-health-support.html">Gut Health Support</a></li><li><a href="{p}weight-metabolic-health.html">Weight Loss &amp; Metabolic Health</a></li><li><a href="{p}hormone-balance-support.html">Hormone Balance</a></li><li><a href="{p}inflammation-support.html">Inflammation Support</a></li><li><a href="{p}emotional-overwhelm-nervous-system.html">Emotional Overwhelm &amp; Nervous System Support</a></li><li><a href="{p}neurodivergent-support.html">Neurodivergent Support</a></li></ul></div>
      <div><h5>About</h5><ul><li><a href="{p}about-lynette-wing-renewal-health.html">Meet Lynette Wing</a></li><li><a href="{p}why-a-dragonfly-renewal-health.html">Why a Dragonfly?</a></li><li><a href="{p}naturopathy-homeopathy-holistic-healing.html">What is Naturopathy and Homeopathy?</a></li></ul></div>
      <div><h5>Explore</h5><ul><li><a href="{p}programs-packages.html">Programs &amp; Packages</a></li><li><a href="{p}testimonials.html">Patient Testimonials</a></li><li><a href="{p}blog.html">Blog</a></li><li><a href="{p}contact-renewal-health.html">Contact</a></li></ul></div>
    </div>
    <div class="foot-base">
      <span>&copy; Renewal Health with Lynette Wing</span>
      <span>Personalized naturopathic &amp; homeopathic care</span>
    </div>
  </div>
</footer>"""

POSTS = [
 dict(slug="how-to-surrender-your-burdens-to-god",
      title="It Is Not Mine to Carry: How to Surrender Your Burdens",
      desc="How to surrender your burdens to God: what surrender does in your body, from cortisol to connection, and the burdens that were never yours to carry.",
      cat="Root Cause Health", date="July 22, 2026", hero="surrender-open-hands-sunrise.jpg"),
 dict(slug="vagal-tone-exercises",
      title="Vagal Tone Exercises: Partner With Your Hidden Engine",
      desc="Vagal tone exercises that actually calm your body: the emergency reset, cold exposure, humming, and extended exhales, explained by Lynette Wing.",
      cat="Nervous System", date="July 22, 2026", hero="deep-breathing-vagal-tone-exercise.jpg"),
 dict(slug="spiritual-growth-through-hardship",
      title="When Defeat Becomes a Doorway: Growth Through Hardship",
      desc="Spiritual growth through hardship: why the shaking is not a punishment but a loosening. Edwin Markham, stress wood, and the hidden healing in defeat.",
      cat="Whole-Person Healing", date="July 22, 2026", hero="oak-tree-straining-in-wind.jpg"),
]

def extract(slug):
    src = open(os.path.join(DRAFTS, slug + ".html"), encoding="utf-8").read()
    art = re.search(r'<article class="rh-post">(.*?)</article>', src, re.S).group(1)
    jsonld = "\n".join(re.findall(r'<script type="application/ld\+json">.*?</script>', src, re.S))
    # drop hero img, first h1, byline p
    art = re.sub(r'<h1[^>]*>.*?</h1>', '', art, count=1, flags=re.S)
    art = re.sub(r'<p style="color:#7a8374[^"]*">.*?</p>', '', art, count=1, flags=re.S)
    art = re.sub(r'<img [^>]*?src="\.\./images/[^"]+"[^>]*>', '', art, count=1, flags=re.S)
    # rewrite remaining image paths
    art = art.replace("../images/%s/" % slug, "../assets/blog/%s/" % slug)
    # rewrite site-internal absolute links to local pages
    art = re.sub(r'https://www\.renewalhealth\.life/([a-z0-9\-]+)', r'../\1.html', art)
    # normalise the hardship inline-styled TOC box to a class
    art = art.replace('<div style="background:#f6f7f4;border-radius:6px;padding:1em 1.6em;font-size:.95em;">',
                      '<div class="rh-tocbox">')
    return art.strip(), jsonld

def build_post(p):
    body, jsonld = extract(p["slug"])
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(p['title'])} — Renewal Health with Lynette Wing</title>
<meta name="description" content="{html.escape(p['desc'])}">
<link rel="stylesheet" href="../assets/v2.css">
</head>
<body class="has-hero">
{NAV.format(p='../')}
<main>
<section class="page-hero has-photo ph-quiet">
  <div class="ph-bg"><img src="../assets/blog/{p['slug']}/{p['hero']}" alt="" aria-hidden="true"></div>
  <div class="ph-veil"></div>
  <div class="inner">
    <p class="eyebrow">{p['cat']}</p>
    <h1>{html.escape(p['title'])}</h1>
    <p class="post-byline">By Lynette Wing, Clinical Homeopath, Naturopath, Mind-Body Practitioner &middot; {p['date']}</p>
  </div>
</section>
<section class="section article intro-reveal"><div class="inner narrow flow">
<a class="post-back" href="../blog.html">&larr; Back to the blog</a>
{body}
</div></section>
<section class="section bg-cream"><div class="inner">
  <div class="cta-panel reveal">
    <h2 class="serif">Start Your Renewal</h2>
    <a class="btn btn-light" href="../contact-renewal-health.html">Contact Me to Schedule Your Consultation!</a>
  </div>
</div></section>
</main>
{FOOTER.format(p='../')}
<script src="../assets/v2.js"></script>
{jsonld}
</body>
</html>"""
    open(os.path.join(ROOT, "blog", p["slug"] + ".html"), "w", encoding="utf-8").write(page)
    print("post", p["slug"])

for p in POSTS:
    build_post(p)
print("done")
