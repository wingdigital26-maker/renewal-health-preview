"""Extract visible text + head metadata from rebuilt pages for before/after diffing."""
import re, sys, os, json, glob, html

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = sorted([os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html"))
                if os.path.basename(p) != "cart.html"])
PAGES.append(os.path.join("blog", "root-cause-healing-naturopathy-homeopathy.html"))


def visible(src):
    s = re.sub(r"(?is)<script.*?</script>", " ", src)
    s = re.sub(r"(?is)<style.*?</style>", " ", s)
    s = re.sub(r"(?is)<head.*?</head>", " ", s)
    s = re.sub(r"(?is)<svg.*?</svg>", " ", s)
    s = re.sub(r"(?s)<!--.*?-->", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    return s.split()


def meta(src):
    t = re.search(r"(?is)<title>(.*?)</title>", src)
    d = re.search(r'(?is)<meta name="description" content="(.*?)">', src)
    h1 = re.findall(r"(?is)<h1[^>]*>(.*?)</h1>", src)
    return {"title": t.group(1) if t else None,
            "desc": d.group(1) if d else None,
            "h1count": len(h1)}


out = {}
for p in PAGES:
    fp = os.path.join(ROOT, p)
    if not os.path.exists(fp):
        continue
    src = open(fp, encoding="utf-8").read()
    m = meta(src)
    m["words"] = visible(src)
    out[p.replace("\\", "/")] = m

dest = sys.argv[1]
json.dump(out, open(dest, "w", encoding="utf-8"), ensure_ascii=False)
print("wrote", dest, len(out), "pages,", sum(len(v["words"]) for v in out.values()), "words")
