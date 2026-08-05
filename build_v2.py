# -*- coding: utf-8 -*-
"""Rebuild Renewal Health site-v2 pages with the new design system.
Extracts every content block verbatim from the Squarespace mirror pages,
then regenerates clean HTML using the v2 shell. Copy is byte-preserved."""
import os, re, html as H
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = r"C:\Users\wjack\seo-factory\renewal-health\site-v2"
SRC = r"C:\Users\wjack\seo-factory\renewal-health\site-mirror"
LOGO = "assets/images.squarespace-cdn.com/content/v1/69de66d56f606e4d8a63fcb5/1557bced-4e06-4bfe-9242-8937f45cbe3d/renewalhealth2stack.jpg"

PAGES = [
    "index.html","home.html","about-lynette-wing-renewal-health.html","about.html",
    "naturopathic-detox.html","gut-health-support.html",
    "weight-metabolic-health.html","hormone-balance-support.html",
    "inflammation-support.html","emotional-overwhelm-nervous-system.html",
    "neurodivergent-support.html","programs-packages.html","services.html",
    "naturopathy-homeopathy-holistic-healing.html","testimonials.html",
    "why-a-dragonfly-renewal-health.html","contact-renewal-health.html",
    "blog.html","resources.html",
    os.path.join("blog","root-cause-healing-naturopathy-homeopathy.html"),
]

INLINE_KEEP = {"a","strong","em","b","i","br","u"}

def inline_html(el, prefix=""):
    out = []
    for node in el.children:
        if isinstance(node, NavigableString):
            out.append(H.escape(str(node)))
        elif isinstance(node, Tag):
            if node.name == "br":
                out.append("<br>")
            elif node.name in INLINE_KEEP and node.name != "br":
                inner = inline_html(node, prefix)
                if node.name == "a" and node.get("href"):
                    href = node["href"]
                    out.append('<a href="%s">%s</a>' % (H.escape(href), inner))
                else:
                    t = node.name if node.name not in ("b","i") else {"b":"strong","i":"em"}[node.name]
                    out.append("<%s>%s</%s>" % (t, inner, t))
            else:
                out.append(inline_html(node, prefix))
    return "".join(out)

def is_button(a):
    cls = " ".join(a.get("class", []))
    return "button" in cls.lower() or "btn" in cls.lower()

def extract(path):
    soup = BeautifulSoup(open(path, encoding="utf8"), "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    md = soup.find("meta", attrs={"name": "description"})
    meta = md["content"].strip() if md and md.get("content") else ""
    art = soup.select_one("article.sections") or soup.find("main") or soup.body
    blocks = []
    seen_imgs = set()
    for el in art.find_all(["h1","h2","h3","h4","p","ul","ol","blockquote","img","a"]):
        # skip elements nested inside blocks we already capture whole
        if el.name != "img" and el.find_parent(["blockquote","li","p","h1","h2","h3","h4"]):
            continue
        if el.name == "img":
            src = el.get("src") or el.get("data-src") or ""
            src = src.split("?")[0]
            if not src or "renewalhealth2stack" in src or src in seen_imgs:
                continue
            seen_imgs.add(src)
            alt = el.get("alt") or re.sub(r"[-_]+"," ",os.path.splitext(os.path.basename(src))[0])
            blocks.append(("img", src, alt))
        elif el.name == "a":
            if is_button(el) and el.get_text(strip=True):
                href = (el.get("href") or "#").split("?")[0]
                blocks.append(("btn", el.get_text(" ", strip=True), href))
        elif el.name in ("ul","ol"):
            if el.find_parent("nav") or not el.get_text(strip=True):
                continue
            items = [inline_html(li) for li in el.find_all("li", recursive=False)]
            if items:
                blocks.append(("list", el.name, items))
        else:
            txt = el.get_text(" ", strip=True)
            if not txt:
                continue
            if el.find_parent(["nav","footer","header"]):
                continue
            blocks.append((el.name, inline_html(el)))
    # dedupe exact consecutive repeats
    out = []
    for b in blocks:
        if out and out[-1] == b:
            continue
        out.append(b)
    return title, meta, out

# ---------------------------------------------------------------- shell
def dragonfly_svg(cls="hero-dragonfly", style="", size=170):
    return f'''<svg class="{cls}" style="{style}" width="{size}" height="{size}" viewBox="0 0 100 100" fill="none" aria-hidden="true">
  <g stroke="currentColor" stroke-width="1.6" stroke-linecap="round">
    <ellipse class="wing" cx="32" cy="38" rx="24" ry="9" transform="rotate(-24 32 38)" fill="currentColor" fill-opacity=".14"/>
    <ellipse class="wing w2" cx="68" cy="38" rx="24" ry="9" transform="rotate(24 68 38)" fill="currentColor" fill-opacity=".14"/>
    <ellipse class="wing w2" cx="34" cy="52" rx="20" ry="7.5" transform="rotate(-38 34 52)" fill="currentColor" fill-opacity=".1"/>
    <ellipse class="wing" cx="66" cy="52" rx="20" ry="7.5" transform="rotate(38 66 52)" fill="currentColor" fill-opacity=".1"/>
    <circle cx="50" cy="30" r="4.5" fill="currentColor"/>
    <path d="M50 35 L50 88" stroke-width="3"/>
    <path d="M47 84 L50 92 L53 84" stroke-width="2"/>
  </g>
</svg>'''

SERVICES = [
    ("Services Overview","services.html"),
    ("Detox","naturopathic-detox.html"),
    ("Gut Health Support","gut-health-support.html"),
    ("Weight Loss & Metabolic Health","weight-metabolic-health.html"),
    ("Hormone Balance","hormone-balance-support.html"),
    ("Inflammation Support","inflammation-support.html"),
    ("Emotional Overwhelm & Nervous System Support","emotional-overwhelm-nervous-system.html"),
    ("Neurodivergent Support","neurodivergent-support.html"),
]
ABOUT = [
    ("Meet Lynette Wing","about-lynette-wing-renewal-health.html"),
    ("Why a Dragonfly?","why-a-dragonfly-renewal-health.html"),
    ("What is Naturopathy and Homeopathy?","naturopathy-homeopathy-holistic-healing.html"),
]

def header(prefix=""):
    def li(items):
        return "".join(f'<li><a href="{prefix}{h}">{H.escape(t)}</a></li>' for t,h in items)
    return f'''<header class="v2-header">
  <div class="bar">
    <a class="v2-logo" href="{prefix}index.html"><img src="{prefix}{LOGO}" alt="Renewal Health with Lynette Wing"></a>
    <nav class="v2-nav" aria-label="Main navigation">
      <ul>
        <li><a href="{prefix}index.html">Home</a></li>
        <li class="has-drop"><a href="{prefix}services.html">Services</a>
          <ul class="dropdown">{li(SERVICES)}</ul></li>
        <li><a href="{prefix}programs-packages.html">Programs &amp; Packages</a></li>
        <li class="has-drop"><a href="{prefix}about-lynette-wing-renewal-health.html">About</a>
          <ul class="dropdown">{li(ABOUT)}</ul></li>
        <li><a href="{prefix}testimonials.html">Testimonials</a></li>
        <li><a href="{prefix}blog.html">Blog</a></li>
      </ul>
      <a class="btn btn-primary nav-cta" href="{prefix}contact-renewal-health.html">Contact</a>
    </nav>
    <button class="nav-toggle" aria-label="Menu"><span></span><span></span><span></span></button>
  </div>
</header>'''

def footer(prefix=""):
    def li(items):
        return "".join(f'<li><a href="{prefix}{h}">{H.escape(t)}</a></li>' for t,h in items)
    return f'''<footer class="v2-footer">
  <div class="inner">
    <div class="foot-grid">
      <div>
        <span class="foot-logo"><img src="{prefix}{LOGO}" alt="Renewal Health with Lynette Wing"></span>
        <p class="foot-tag">Emerge. Align. Live Fully.</p>
      </div>
      <div><h5>Services</h5><ul>{li(SERVICES[1:])}</ul></div>
      <div><h5>About</h5><ul>{li(ABOUT)}</ul></div>
      <div><h5>Explore</h5><ul>{li([("Programs & Packages","programs-packages.html"),("Patient Testimonials","testimonials.html"),("Blog","blog.html"),("Contact","contact-renewal-health.html")])}</ul></div>
    </div>
    <div class="foot-base">
      <span>&copy; Renewal Health with Lynette Wing</span>
      <span>Personalized naturopathic &amp; homeopathic care</span>
    </div>
  </div>
</footer>
<script src="{prefix}assets/v2.js"></script>'''

def page_shell(title, meta, body, prefix=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{H.escape(title)}</title>
<meta name="description" content="{H.escape(meta)}">
<link rel="stylesheet" href="{prefix}assets/v2.css">
</head>
<body>
{header(prefix)}
<main>
{body}
</main>
{footer(prefix)}
</body>
</html>'''

# ---------------------------------------------------------- interior pages
def pfx(prefix, path):
    return path if path.startswith(("../","http","#","mailto")) else prefix + path

def render_blocks(blocks, prefix=""):
    out = []
    for b in blocks:
        if b[0] == "img":
            out.append(f'<figure class="reveal"><img src="{H.escape(pfx(prefix,b[1]))}" alt="{H.escape(b[2])}" loading="lazy"></figure>')
        elif b[0] == "btn":
            out.append(f'<a class="btn btn-primary reveal" href="{H.escape(pfx(prefix,b[2]))}">{H.escape(b[1])}</a>')
        elif b[0] == "list":
            items = "".join(f"<li>{i}</li>" for i in b[2])
            out.append(f'<{b[1]} class="checks reveal">{items}</{b[1]}>')
        elif b[0] in ("h2","h3","h4"):
            out.append(f'<{b[0]} class="reveal">{b[1]}</{b[0]}>')
        elif b[0] == "blockquote":
            out.append(f'<blockquote class="reveal">{b[1]}</blockquote>')
        else:
            out.append(f"<p>{b[1]}</p>")
    return "\n".join(out)

BG_CYCLE = ["bg-cream","bg-white","bg-sage","bg-white"]

def build_interior(src, dst=None, prefix=""):
    title, meta, blocks = extract(os.path.join(SRC, src))
    # hero = h1 + everything before first h2
    h1 = next((b for b in blocks if b[0] == "h1"), None)
    h1_html = h1[1] if h1 else ""
    rest = [b for b in blocks if b is not h1]
    # lede: leading paragraphs before first h2/img go into hero
    lede = []
    while rest and rest[0][0] == "p" and len(lede) < 3:
        lede.append(rest.pop(0))
    lede_html = "".join(f'<p class="lede">{p[1]}</p>' for p in lede)
    # chunk remaining into sections at h2 boundaries
    sections, cur = [], []
    for b in rest:
        if b[0] == "h2" and cur:
            sections.append(cur); cur = [b]
        else:
            cur.append(b)
    if cur: sections.append(cur)
    body = [f'''<section class="page-hero">
  {dragonfly_svg(style="top:8%;left:6%;color:#fff;")}
  {dragonfly_svg(style="bottom:10%;right:7%;color:#b79cc9;animation-delay:-7s;", size=120)}
  <div class="inner">
    <h1>{h1_html}</h1>
    {lede_html}
  </div>
</section>''']
    for i, sec in enumerate(sections):
        bg = BG_CYCLE[i % len(BG_CYCLE)]
        body.append(f'<section class="section {bg}"><div class="inner narrow flow">\n{render_blocks(sec, prefix)}\n</div></section>')
    # closing CTA
    body.append(f'''<section class="section bg-cream"><div class="inner">
  <div class="cta-panel reveal">
    {dragonfly_svg(style="top:-20px;right:4%;color:#fff;opacity:.12;", size=140)}
    <h2 class="serif">Start Your Renewal</h2>
    <a class="btn btn-light" href="{prefix}contact-renewal-health.html">Contact Me to Schedule Your Consultation!</a>
  </div>
</div></section>''')
    out = page_shell(title, meta, "\n".join(body), prefix)
    dstp = os.path.join(ROOT, dst or src)
    open(dstp, "w", encoding="utf8").write(out)
    print("wrote", dst or src, len(out))

# ---------------------------------------------------------------- home page
def build_home():
    title, meta, blocks = extract(os.path.join(SRC, "index.html"))
    def take(kind=None, startswith=None):
        for i, b in enumerate(blocks):
            if kind and b[0] != kind: continue
            if startswith and not re.sub(r"<[^>]+>","",b[1] if len(b)>1 else "").strip().startswith(startswith): continue
            return blocks.pop(i)
        raise SystemExit("missing block %s %s" % (kind, startswith))
    hero_img  = take("img")
    h1        = take("h1")
    hero_sub  = take("h2")
    btn_df    = take("btn")
    s2_h      = take("h2", "You are meant")
    s2_ps     = [take("p") for _ in range(3)]
    img2      = take("img")
    s3_h      = take("h2", "A root-cause approach")
    s3_ps     = [take("p") for _ in range(3)]
    s4_h      = take("h2", "What you may be experiencing")
    s4_intro  = take("p", "You might recognize")
    try:
        lst = take("list")
        s4_items = [("p", i) for i in lst[2]]
    except SystemExit:
        s4_items = [take("p") for _ in range(4)]
    s4_close  = take("p", "If that resonates")
    svc_h     = take("h2", "Personalized support")
    cards = []
    for _ in range(7):
        cards.append((take("h3"), take("p"), take("btn")))
    img3      = take("img")
    proc_h    = take("h2", "A personalized process")
    proc_sub  = take("h3", "How Your Renewal")
    steps = []
    for _ in range(4):
        steps.append((take("h4"), take("p")))
    pers_h    = take("h3", "Personalized, Holistic")
    pers_ps   = [take("p") for _ in range(2)]
    align_h   = take("h2", "When Your Health Aligns")
    align_ps  = [take("p") for _ in range(2)]
    start_h   = take("h3", "Start Your Renewal")
    start_p   = take("p")
    start_btn = take("btn")

    icons = {
        "Detox":'<svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 3c-3.5 4-6 6.8-6 10a6 6 0 0 0 12 0c0-3.2-2.5-6-6-10z"/></svg>',
        "Hormones":'<svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="8" cy="12" r="4.5"/><circle cx="16" cy="12" r="4.5"/></svg>',
        "Gut Health":'<svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 8c0-2 2-4 5-4h6c3 0 5 2 5 4s-2 4-5 4H9c-2 0-3 1-3 2s1 2 3 2h9"/></svg>',
        "Inflammation":'<svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"/><circle cx="12" cy="12" r="3.5"/></svg>',
        "Neurodivergent Care":'<svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 4a4 4 0 0 0-4 4v1a3 3 0 0 0 0 6v1a4 4 0 0 0 8 0V4a4 4 0 0 0-4 0z"/><path d="M15 4a4 4 0 0 1 4 4v1a3 3 0 0 1 0 6v1a4 4 0 0 1-4 4"/></svg>',
        "Weight":'<svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 4h12l2 16H4L6 4z"/><path d="M9 8a3 3 0 0 0 6 0"/></svg>',
        "Emotional Overwhelm":'<svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/></svg>',
    }
    card_html = ""
    for (h3, p, btn) in cards:
        name = re.sub(r"<[^>]+>","",h3[1]).strip()
        ic = icons.get(name, "")
        card_html += f'''<article class="card reveal">
      {ic}<h3>{h3[1]}</h3><p>{p[1]}</p>
      <a class="text-link" href="{H.escape(btn[2])}">{H.escape(btn[1])}</a>
    </article>\n'''

    steps_html = "".join(
        f'''<div class="step reveal d{i}">
        <div class="step-num">0{i+1}</div>
        <h4>{re.sub(r"^[0-9]+[.]\\s*","",h4[1])}</h4><p>{p[1]}</p>
      </div>''' for i,(h4,p) in enumerate(steps))

    body = f'''
<section class="home-hero">
  <div class="home-hero-bg"><img src="{H.escape(hero_img[1])}" alt="Dragonfly resting on a grass stem" data-parallax></div>
  <div class="home-hero-veil"></div>
  {dragonfly_svg(style="top:14%;left:8%;color:#e8dff0;", size=150)}
  {dragonfly_svg(style="top:58%;right:10%;color:#b79cc9;animation-delay:-6s;", size=100)}
  {dragonfly_svg(style="bottom:12%;left:22%;color:#8fae85;animation-delay:-10s;", size=70)}
  <div class="home-hero-content">
    <p class="eyebrow reveal in">Naturopathic &amp; Homeopathic Care</p>
    <h1 class="reveal in">{h1[1]}</h1>
    <p class="home-hero-lede reveal in d1">{hero_sub[1]}</p>
    <div class="reveal in d2">
      <a class="btn btn-light" href="contact-renewal-health.html">{H.escape(start_btn[1])}</a>
      <a class="btn btn-ghost btn-ghost-light" href="{H.escape(btn_df[2])}">{H.escape(btn_df[1])}</a>
    </div>
  </div>
  <div class="scroll-hint" aria-hidden="true"><span></span></div>
</section>

<div class="word-band" aria-hidden="true">
  <div class="track">
    <span>Emerge</span><span>Align</span><span>Live Fully</span><span>Renewal Health</span>
    <span>Emerge</span><span>Align</span><span>Live Fully</span><span>Renewal Health</span>
  </div>
</div>

<section class="section bg-cream">
  <div class="inner split">
    <div class="reveal">
      <p class="eyebrow">A Different Kind of Support</p>
      <h2>{s2_h[1]}</h2>
      {"".join(f"<p>{p[1]}</p>" for p in s2_ps)}
    </div>
    <div class="media reveal d1"><div class="media-frame"><img src="{H.escape(img2[1])}" alt="Interconnected holistic health" loading="lazy"></div></div>
  </div>
</section>

<section class="section bg-white">
  <div class="inner split rev">
    <div class="reveal">
      <p class="eyebrow">Root-Cause Care</p>
      <h2>{s3_h[1]}</h2>
      {"".join(f"<p>{p[1]}</p>" for p in s3_ps)}
    </div>
    <div class="media reveal d1">
      <div class="check-card">
        <h3>{s4_h[1]}</h3>
        <p>{s4_intro[1]}</p>
        <ul>{"".join(f"<li>{p[1]}</li>" for p in s4_items)}</ul>
        <p><em>{s4_close[1]}</em></p>
      </div>
    </div>
  </div>
</section>

<section class="section bg-sage">
  <div class="inner section-center">
    <p class="eyebrow reveal">Services</p>
    <h2 class="reveal" style="max-width:860px;margin-left:auto;margin-right:auto">{svc_h[1]}</h2>
    <div class="card-grid" style="text-align:left">
{card_html}    </div>
  </div>
</section>

<section class="section bg-white">
  <div class="inner">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">{re.sub(r"<[^>]+>","",proc_sub[1])}</p>
        <h2>{proc_h[1]}</h2>
        <h3 style="margin-top:1.2em">{pers_h[1]}</h3>
        {"".join(f"<p>{p[1]}</p>" for p in pers_ps)}
      </div>
      <div class="media reveal d1"><div class="media-frame"><img src="{H.escape(img3[1])}" alt="Calm natural scene" loading="lazy"></div></div>
    </div>
    <div class="steps">{steps_html}</div>
  </div>
</section>

<section class="section bg-cream">
  <div class="inner">
    <div class="cta-panel reveal">
      {dragonfly_svg(style="top:-16px;right:5%;color:#fff;opacity:.14;", size=150)}
      {dragonfly_svg(style="bottom:-10px;left:4%;color:#8fae85;opacity:.2;animation-delay:-5s;", size=100)}
      <h2>{align_h[1]}</h2>
      {"".join(f"<p>{p[1]}</p>" for p in align_ps)}
      <h3 style="margin-top:1.6rem">{start_h[1]}</h3>
      <p>{start_p[1]}</p>
      <a class="btn btn-light" href="{H.escape(start_btn[2])}">{H.escape(start_btn[1])}</a>
    </div>
  </div>
</section>
'''
    extra_css = '''<style>
.home-hero{position:relative;min-height:92vh;display:flex;align-items:center;justify-content:center;text-align:center;overflow:hidden;color:#fff}
.home-hero-bg{position:absolute;inset:0}
.home-hero-bg img{width:100%;height:110%;object-fit:cover;transform:scale(1.04)}
.home-hero-veil{position:absolute;inset:0;background:linear-gradient(160deg,rgba(45,27,56,.82) 0%,rgba(75,46,90,.55) 45%,rgba(45,27,56,.78) 100%)}
.home-hero-content{position:relative;z-index:2;max-width:900px;padding:6rem 1.4rem}
.home-hero h1{color:#fff;font-size:clamp(3rem,8vw,5.6rem);font-weight:600;letter-spacing:-.015em;text-shadow:0 4px 40px rgba(0,0,0,.35)}
.home-hero-lede{font-family:var(--serif);font-size:clamp(1.15rem,2.2vw,1.55rem);color:#e8dff0;max-width:640px;margin:1.4rem auto 2.2rem;font-style:italic}
.home-hero .eyebrow{color:#b79cc9;justify-content:center}
.home-hero .eyebrow::before{background:#b79cc9}
.home-hero .btn{margin:.4rem .5rem}
.btn-ghost-light{border-color:rgba(255,255,255,.7);color:#fff}
.btn-ghost-light:hover{background:#fff;color:var(--plum)}
.scroll-hint{position:absolute;bottom:2rem;left:50%;transform:translateX(-50%);z-index:2}
.scroll-hint span{display:block;width:1.5px;height:44px;background:linear-gradient(#fff,transparent);animation:hint 2s ease-in-out infinite}
@keyframes hint{0%{transform:scaleY(0);transform-origin:top}45%{transform:scaleY(1);transform-origin:top}55%{transform:scaleY(1);transform-origin:bottom}100%{transform:scaleY(0);transform-origin:bottom}}
</style>'''
    out = page_shell(title, meta, body).replace("</head>", extra_css + "\n</head>")
    for dst in ("index.html","home.html"):
        open(os.path.join(ROOT,dst),"w",encoding="utf8").write(out)
        print("wrote",dst,len(out))

# ---------------------------------------------------------------- run
build_home()
for p in PAGES:
    if p in ("index.html","home.html"): continue
    prefix = "../" if os.sep in p else ""
    build_interior(p, prefix=prefix)
print("done")
