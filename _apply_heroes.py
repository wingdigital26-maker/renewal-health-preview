# -*- coding: utf-8 -*-
"""Inject distinct photo-backed heroes per page and replace the reused
inline dragonfly figure on interior pages. Pure structural change: no
body copy is touched (only image src/alt attributes and hero wrapper)."""
import re, os

ROOT = os.path.dirname(os.path.abspath(__file__))
DRAGONFLY = "assets/images.squarespace-cdn.com/content/v1/69de66d56f606e4d8a63fcb5/1591e378-1aba-426a-b433-aa793fdb2f24/pexels-depthofraw-10722719.jpg"

# page -> (hero image, hero alt, inline replacement image, inline alt)
HERO = {
 "naturopathic-detox.html": ("hero-detox-herbal-botanical","Botanical herbal infusion with soft petals","hero-gut-green-fern","Soft green fern fronds"),
 "services.html": ("hero-services-eucalyptus","Fresh eucalyptus branch on a pale ground","hero-inflammation-eucalyptus-leaf","Eucalyptus leaves resting on still water"),
 "gut-health-support.html": ("hero-gut-green-fern","Unfurling green fern fronds","hero-programs-tea-pour","Herbal tea being poured gently"),
 "weight-metabolic-health.html": ("hero-weight-succulents","Calm cluster of green succulents","hero-naturopathy-dried-herbs","Dried herbs arranged on wooden spoons"),
 "hormone-balance-support.html": ("hero-hormone-lavender","Lavender field in soft summer light","hero-contact-chamomile","Chamomile flowers floating in a bowl"),
 "inflammation-support.html": ("hero-inflammation-eucalyptus-leaf","Eucalyptus leaves resting on still water","hero-neuro-green-foliage","Lush layered green foliage"),
 "emotional-overwhelm-nervous-system.html": ("hero-emotional-calm-water","Gentle ripples spreading across calm water","hero-dragonfly-lake","Still lake reflecting the dawn sky"),
 "neurodivergent-support.html": ("hero-neuro-green-foliage","Lush layered green foliage","hero-weight-succulents","Calm cluster of green succulents"),
 "about-lynette-wing-renewal-health.html": ("hero-about-waterlily","Water lilies resting on a still pond",None,None),
 "about.html": ("hero-about-waterlily","Water lilies resting on a still pond",None,None),
 "why-a-dragonfly-renewal-health.html": ("hero-dragonfly-lake","Still lake reflecting the dawn sky","hero-emotional-calm-water","Gentle ripples across calm water"),
 "naturopathy-homeopathy-holistic-healing.html": ("hero-naturopathy-dried-herbs","Dried herbs arranged on wooden spoons","hero-detox-herbal-botanical","Botanical herbal infusion with soft petals"),
 "programs-packages.html": ("hero-programs-tea-pour","Herbal tea being poured gently",None,None),
 "contact-renewal-health.html": ("hero-contact-chamomile","Chamomile flowers floating in a bowl",None,None),
 "blog.html": ("hero-blog-lavender-summer","Lavender in soft summer light",None,None),
}

def inject_hero(src, hero_img, hero_alt):
    def repl(m):
        cls = m.group(1)  # extra classes after page-hero
        bg = ('<div class="ph-bg"><img src="assets/heroes/%s.jpg" alt="" aria-hidden="true"></div>'
              '<div class="ph-veil"></div>' % hero_img)
        return '<section class="page-hero has-photo%s">\n  %s\n' % (cls, bg)
    return re.sub(r'<section class="page-hero([^"]*)">\s*', repl, src, count=1)

def main():
    for page,(hi,ha,ii,ia) in HERO.items():
        fp=os.path.join(ROOT,page)
        if not os.path.exists(fp):
            print("skip missing",page); continue
        s=open(fp,encoding="utf-8").read()
        before=s
        s=inject_hero(s,hi,ha)
        # replace the reused inline dragonfly figure image (interior pages only)
        if ii and DRAGONFLY in s:
            s=s.replace(
                '<img src="%s" alt="pexels depthofraw 10722719" loading="lazy">'%DRAGONFLY,
                '<img src="assets/heroes/%s.jpg" alt="%s" loading="lazy">'%(ii,ia))
        if s!=before:
            open(fp,"w",encoding="utf-8").write(s)
            print("done",page)
        else:
            print("NOCHANGE",page)

if __name__=="__main__":
    main()
