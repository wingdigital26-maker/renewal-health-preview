# -*- coding: utf-8 -*-
"""Generate the naturalistic vector dragonfly used for the home hero entrance.

Everything is authored here as maths so the wing venation is genuinely dense
(longitudinal veins plus a staggered cross-vein mesh, exactly like a real
odonate wing) rather than a handful of decorative strokes. Output is written
to _hero_entrance.part and injected into index.html / home.html by
_inject_hero.py. No raster asset, no external request.
"""
import math

W, H = 960, 640
AX = 268.0  # body axis y


def bez(p0, p1, p2, t):
    mt = 1 - t
    return (mt * mt * p0[0] + 2 * mt * t * p1[0] + t * t * p2[0],
            mt * mt * p0[1] + 2 * mt * t * p1[1] + t * t * p2[1])


def dbez(p0, p1, p2, t):
    mt = 1 - t
    return (2 * mt * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0]),
            2 * mt * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1]))


class Wing(object):
    """A wing is a quadratic spine plus a width profile measured normal to it."""

    def __init__(self, base, ctrl, tip, wmax, swell=0.42, flip=1):
        self.p0, self.p1, self.p2 = base, ctrl, tip
        self.wmax = wmax
        self.swell = swell
        self.flip = flip

    def width(self, u):
        # narrow at the articulation, broadest just past mid-wing, tapering to
        # a rounded apex: the classic anisopteran blade.
        a = math.sin(math.pi * min(1.0, (u * 0.62 + 0.16))) ** 0.72
        b = 0.34 + 0.66 * math.sin(math.pi * (0.15 + 0.85 * u)) ** 0.5
        return self.wmax * (0.14 + 0.86 * a) * b * (1 - 0.55 * u ** 2.4)

    def point(self, u, v):
        cx, cy = bez(self.p0, self.p1, self.p2, u)
        dx, dy = dbez(self.p0, self.p1, self.p2, u)
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        w = self.width(u)
        # leading edge (v=-1) is straighter than the trailing edge (v=+1)
        k = 1.0 if v >= 0 else 0.78
        return (cx + nx * w * v * k, cy + ny * w * v * k)

    def outline(self, n=48):
        pts = [self.point(u / float(n), -1.0) for u in range(n + 1)]
        # rounded apex
        for i in range(1, 8):
            a = -1.0 + 2.0 * i / 8.0
            pts.append(self.point(1.0 - 0.004 * (1 - abs(a)), a))
        pts += [self.point(u / float(n), 1.0) for u in range(n, -1, -1)]
        d = "M%d %d" % pts[0]
        for p in pts[1:]:
            d += "L%d %d" % p
        return d + "Z"

    def longitudinal(self, vs, n=34, u0=0.03, u1=0.985):
        out = []
        for v in vs:
            pts = []
            for i in range(n + 1):
                u = u0 + (u1 - u0) * i / float(n)
                pts.append(self.point(u, v * (0.30 + 0.70 * min(1.0, u * 2.2))))
            d = "M%d %d" % pts[0]
            for p in pts[1:]:
                d += "L%d %d" % p
            out.append(d)
        return out

    def crossveins(self, vs, step=0.026, u0=0.06, u1=0.965):
        out = []
        for j in range(len(vs) - 1):
            va, vb = vs[j], vs[j + 1]
            u = u0 + (j % 2) * step * 0.5
            while u < u1:
                sa = 0.30 + 0.70 * min(1.0, u * 2.2)
                pa = self.point(u, va * sa)
                pb = self.point(u + step * 0.42, vb * sa)
                out.append("M%d %dL%d %d" % (pa[0], pa[1], pb[0], pb[1]))
                u += step
        return out

    def stigma(self, u=0.878, span=0.056):
        pts = []
        for i in range(9):
            uu = u + span * i / 8.0
            pts.append(self.point(uu, -0.985))
        for i in range(8, -1, -1):
            uu = u + span * i / 8.0
            pts.append(self.point(uu, -0.70))
        d = "M%d %d" % pts[0]
        for p in pts[1:]:
            d += "L%d %d" % p
        return d + "Z"


VS = [-0.88, -0.66, -0.44, -0.22, 0.0, 0.24, 0.48, 0.72, 0.9]

# Four wings. Forewings sit slightly ahead of and above the hindwings, which is
# what makes a dragonfly read as a dragonfly rather than a butterfly.
WINGS = {
    "fore-up":  Wing((742, 250), (470, 92), (168, 74), 60),
    "hind-up":  Wing((706, 262), (452, 150), (150, 156), 66),
    "fore-dn":  Wing((738, 286), (474, 396), (176, 452), 58),
    "hind-dn":  Wing((702, 296), (450, 372), (146, 500), 64),
}


KEYCLIP = {"fore-up": "fu", "hind-up": "hu", "fore-dn": "fd", "hind-dn": "hd"}


def wing_group(name, key, grad, vein, opacity):
    w = WINGS[key]
    cid = "clip-" + KEYCLIP[key]
    s = []
    s.append('    <g class="wing wing-%s">' % name)
    s.append('      <path class="wing-mem" d="%s" fill="url(#%s)" stroke="#efe6f7" '
             'stroke-opacity=".55" stroke-width="1.4" opacity="%s"/>' % (w.outline(), grad, opacity))
    s.append('      <g clip-path="url(#%s)">' % cid)
    s.append('        <path d="%s" fill="url(#iri)" opacity=".55"/>' % w.outline())
    s.append('        <g stroke="%s" stroke-opacity=".58" stroke-width="1.5" fill="none" '
             'stroke-linecap="round">' % vein)
    for d in w.longitudinal(VS):
        s.append('          <path d="%s"/>' % d)
    s.append('        </g>')
    s.append('        <g stroke="%s" stroke-opacity=".40" stroke-width=".9" fill="none">' % vein)
    for d in w.crossveins(VS):
        s.append('          <path d="%s"/>' % d)
    s.append('        </g>')
    s.append('      </g>')
    # costal (leading-edge) vein: the thickest vein on a real wing
    lead = w.longitudinal([-1.0], n=60)[0]
    s.append('      <path d="%s" stroke="%s" stroke-opacity=".62" stroke-width="2.6" '
             'fill="none" stroke-linecap="round"/>' % (lead, vein))
    s.append('      <path d="%s" fill="#3a2352" opacity=".9"/>' % w.stigma())
    s.append('    </g>')
    return "\n".join(s)


def clip(name, key):
    return ('    <clipPath id="clip-%s"><path d="%s"/></clipPath>'
            % (name, WINGS[key].outline()))


def abdomen():
    """Ten tapered segments with the real S7 to S8 pinch and a slight club."""
    top, bot = [], []
    x0, x1 = 92.0, 700.0
    for i in range(61):
        t = i / 60.0
        x = x1 - (x1 - x0) * t
        # thickness profile from thorax (t=0) to the cerci (t=1)
        r = 25.0 * (1 - t) ** 0.62 + 5.6
        r *= 1.0 + 0.20 * math.exp(-((t - 0.80) ** 2) / 0.006)   # club at S8
        r *= 1.0 - 0.16 * math.exp(-((t - 0.60) ** 2) / 0.004)   # pinch at S6
        droop = 16.0 * t ** 2.1
        top.append((x, AX - r + droop))
        bot.append((x, AX + r + droop))
    pts = top + bot[::-1]
    d = "M%d %d" % pts[0]
    for p in pts[1:]:
        d += "L%d %d" % p
    return d + "Z", top, bot


def segments(top, bot):
    out = []
    for i in range(4, 60, 6):
        a, b = top[i], bot[i]
        out.append("M%d %dL%d %d" % (a[0], a[1], b[0], b[1]))
    return out


def build():
    ab, top, bot = abdomen()
    segs = segments(top, bot)
    L = []
    A = L.append
    A('<!-- hero entrance: blue-violet curtain + naturalistic vector dragonfly '
      '(both removed by v2.js on animationend) -->')
    A('<div class="hero-curtain" aria-hidden="true"></div>')
    A('<svg class="df-reveal" viewBox="0 0 %d %d" aria-hidden="true" focusable="false" '
      'xmlns="http://www.w3.org/2000/svg">' % (W, H))
    A('  <defs>')
    # translucent wing membranes, faintly warm at the base, cool at the apex
    A('    <linearGradient id="memA" x1="88%" y1="46%" x2="10%" y2="6%">')
    A('      <stop offset="0%" stop-color="#fdfbff" stop-opacity=".58"/>')
    A('      <stop offset="34%" stop-color="#f2ecfa" stop-opacity=".46"/>')
    A('      <stop offset="72%" stop-color="#dcd2f0" stop-opacity=".40"/>')
    A('      <stop offset="100%" stop-color="#c3b6e2" stop-opacity=".34"/>')
    A('    </linearGradient>')
    A('    <linearGradient id="memB" x1="88%" y1="54%" x2="10%" y2="96%">')
    A('      <stop offset="0%" stop-color="#fdfbff" stop-opacity=".54"/>')
    A('      <stop offset="38%" stop-color="#eee7f8" stop-opacity=".44"/>')
    A('      <stop offset="100%" stop-color="#bcaee0" stop-opacity=".32"/>')
    A('    </linearGradient>')
    # the iridescent sheen: a hint of blue-violet shifting to teal, as on real
    # dragonfly wings catching the light
    A('    <linearGradient id="iri" x1="90%" y1="20%" x2="6%" y2="88%">')
    A('      <stop offset="0%" stop-color="#8fb7ff" stop-opacity=".00"/>')
    A('      <stop offset="22%" stop-color="#7f9df5" stop-opacity=".30"/>')
    A('      <stop offset="44%" stop-color="#b79cc9" stop-opacity=".16"/>')
    A('      <stop offset="63%" stop-color="#7de0d8" stop-opacity=".18"/>')
    A('      <stop offset="82%" stop-color="#9d8bf0" stop-opacity=".26"/>')
    A('      <stop offset="100%" stop-color="#dcd2f5" stop-opacity=".10"/>')
    A('    </linearGradient>')
    # body: dark iridescent blue-violet with a lit dorsal ridge
    A('    <linearGradient id="abd" x1="0%" y1="0%" x2="0%" y2="100%">')
    A('      <stop offset="0%" stop-color="#1b1440"/>')
    A('      <stop offset="24%" stop-color="#6f5ba8"/>')
    A('      <stop offset="46%" stop-color="#4a3676"/>')
    A('      <stop offset="76%" stop-color="#241a45"/>')
    A('      <stop offset="100%" stop-color="#140e2a"/>')
    A('    </linearGradient>')
    A('    <radialGradient id="thx" cx="42%" cy="28%" r="78%">')
    A('      <stop offset="0%" stop-color="#9d86c8"/>')
    A('      <stop offset="38%" stop-color="#5c4489"/>')
    A('      <stop offset="74%" stop-color="#33244f"/>')
    A('      <stop offset="100%" stop-color="#191031"/>')
    A('    </radialGradient>')
    A('    <radialGradient id="eyeL" cx="34%" cy="26%" r="82%">')
    A('      <stop offset="0%" stop-color="#cfe4ff"/>')
    A('      <stop offset="26%" stop-color="#7fa6e8"/>')
    A('      <stop offset="62%" stop-color="#4a5fae"/>')
    A('      <stop offset="100%" stop-color="#221a44"/>')
    A('    </radialGradient>')
    A('    <radialGradient id="aura" cx="56%" cy="50%" r="54%">')
    A('      <stop offset="0%" stop-color="#a99adf" stop-opacity=".34"/>')
    A('      <stop offset="58%" stop-color="#7f6ec0" stop-opacity=".12"/>')
    A('      <stop offset="100%" stop-color="#7f6ec0" stop-opacity="0"/>')
    A('    </radialGradient>')
    # fine facet texture for the compound eyes
    A('    <pattern id="facets" width="5" height="4" patternUnits="userSpaceOnUse">')
    A('      <path d="M0 2h5M2.5 0v4" stroke="#0e0a20" stroke-opacity=".26" stroke-width=".55"/>')
    A('    </pattern>')
    A('    <filter id="trail" x="-30%" y="-30%" width="160%" height="160%">')
    A('      <feGaussianBlur stdDeviation="7"/>')
    A('    </filter>')
    for n, k in (("fu", "fore-up"), ("hu", "hind-up"), ("fd", "fore-dn"), ("hd", "hind-dn")):
        A(clip(n, k))
    A('  </defs>')
    A('')
    A('  <ellipse cx="470" cy="300" rx="470" ry="300" fill="url(#aura)"/>')
    A('')
    A('  <!-- far wing pair, softened and offset so the four wings read in depth -->')
    A('  <g class="df-far" opacity=".5" transform="translate(-44 42) rotate(-4 742 272) scale(.97)">')
    A(wing_group("hu-far", "hind-up", "memA", "#6f5a92", ".62"))
    A(wing_group("hd-far", "hind-dn", "memB", "#6f5a92", ".58"))
    A('  </g>')
    A('')
    A('  <!-- motion blur: ghosted copies of the beating wings sell the speed -->')
    A('  <g class="df-trail" filter="url(#trail)" opacity=".55" transform="translate(28 14)">')
    A('    <g class="df-trail-a">')
    A(wing_group("fu-t", "fore-up", "memA", "#8e78b4", ".5"))
    A(wing_group("fd-t", "fore-dn", "memB", "#8e78b4", ".5"))
    A('    </g>')
    A('  </g>')
    A('')
    A('  <g class="df-body">')
    A('    <path d="%s" fill="url(#abd)"/>' % ab)
    A('    <g stroke="#0f0a24" stroke-opacity=".26" stroke-width="1.5" fill="none" '
      'stroke-linecap="round">')
    for d in segs:
        A('      <path d="%s"/>' % d)
    A('    </g>')
    # dorsal highlight running the length of the abdomen
    d = "M%d %d" % (top[0][0], top[0][1] + 6)
    for p in top[1:]:
        d += "L%d %d" % (p[0], p[1] + 6)
    A('    <path d="%s" stroke="#cbb8ea" stroke-opacity=".45" stroke-width="3.2" '
      'fill="none" stroke-linecap="round"/>' % d)
    # cerci
    A('    <path d="M96 262c-16-6-30-13-40-23 18 3 34 9 44 16Zm-2 26c-15 8-28 17-36 28 '
      '17-5 32-13 41-21Z" fill="#3b2b5e"/>')
    # thorax
    A('    <ellipse cx="742" cy="272" rx="72" ry="56" fill="url(#thx)" '
      'transform="rotate(-9 742 272)"/>')
    A('    <path d="M700 236c22-18 58-24 86-14-24 2-52 9-72 22Z" fill="#c6b2e6" opacity=".38"/>')
    A('    <g stroke="#1b1236" stroke-opacity=".34" stroke-width="2.2" fill="none">')
    A('      <path d="M716 224c10 28 12 60 4 92"/>')
    A('      <path d="M752 219c9 30 10 62 1 95"/>')
    A('    </g>')
    # legs: six, spined, folded forward under the thorax as in flight
    A('    <g class="df-legs" stroke="#241a45" stroke-opacity=".9" stroke-linecap="round" '
      'fill="none">')
    for d, sw in (("M742 320c-10 30-34 46-66 52", 4.2),
                  ("M768 322c-4 32-24 52-54 62", 3.8),
                  ("M792 316c4 30-10 54-38 68", 3.4),
                  ("M760 318c-16 24-40 36-70 40", 2.6),
                  ("M786 312c-2 26-20 44-46 54", 2.4)):
        A('      <path d="%s" stroke-width="%s"/>' % (d, sw))
    A('    </g>')
    A('    <g stroke="#241a45" stroke-opacity=".55" stroke-width="1.6" fill="none" '
      'stroke-linecap="round">')
    for d in ("M706 336l-8 12M688 344l-7 13M672 350l-6 13",
              "M726 356l-8 12M710 366l-7 12"):
        A('      <path d="%s"/>' % d)
    A('    </g>')
    # head and compound eyes
    A('    <path d="M796 240c34-14 66-4 74 22 8 26-14 50-50 52-32 2-54-14-56-36-2-20 '
      '14-32 32-38Z" fill="#2b1f4c"/>')
    A('    <ellipse cx="846" cy="252" rx="46" ry="37" fill="url(#eyeL)" '
      'transform="rotate(-16 846 252)"/>')
    A('    <ellipse cx="846" cy="252" rx="46" ry="37" fill="url(#facets)" opacity=".34" '
      'transform="rotate(-16 846 252)"/>')
    A('    <ellipse cx="820" cy="292" rx="32" ry="24" fill="url(#eyeL)" opacity=".82" '
      'transform="rotate(-10 820 292)"/>')
    A('    <ellipse cx="820" cy="292" rx="32" ry="24" fill="url(#facets)" opacity=".28" '
      'transform="rotate(-10 820 292)"/>')
    A('    <ellipse cx="858" cy="236" rx="13" ry="8" fill="#ffffff" opacity=".72" '
      'transform="rotate(-22 858 236)"/>')
    A('    <path d="M876 282c10 6 16 14 17 24-8-8-16-15-24-19Z" fill="#3b2b5e"/>')
    A('  </g>')
    A('')
    A('  <!-- near wing pair -->')
    A('  <g class="df-near">')
    A(wing_group("fu", "fore-up", "memA", "#6b5490", ".72"))
    A(wing_group("fd", "fore-dn", "memB", "#6b5490", ".68"))
    A('  </g>')
    A('')
    A('  <!-- shoulder cap: hides the wing articulation so the bases do not flare -->')
    A('  <g class="df-shoulder">')
    A('    <ellipse cx="756" cy="274" rx="46" ry="41" fill="url(#thx)" '
      'transform="rotate(-12 756 274)"/>')
    A('    <path d="M726 250c16-13 42-17 63-10-18 2-39 7-53 16Z" fill="#cbb8ea" opacity=".42"/>')
    A('    <g stroke="#1b1236" stroke-opacity=".3" stroke-width="1.8" fill="none">')
    A('      <path d="M744 236c7 22 8 48 2 74"/><path d="M768 234c6 23 6 48 0 72"/>')
    A('    </g>')
    A('  </g>')
    A('</svg>')
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    out = build()
    open("_hero_entrance.part", "w", encoding="utf-8").write(out)
    print("wrote _hero_entrance.part", len(out), "bytes")
