"""A run of sibling <h3> sections is followed, on some pages, by a concluding
paragraph that belongs to the parent <h2> section rather than to the last <h3>.
The card grouping swallowed those into the final card. This pulls the surplus
trailing <p> blocks back out, after the grid. Words are only moved, never cut."""
import re, sys, html

PAGES = [
    'services.html', 'naturopathic-detox.html', 'gut-health-support.html',
    'weight-metabolic-health.html', 'hormone-balance-support.html',
    'inflammation-support.html', 'emotional-overwhelm-nervous-system.html',
    'neurodivergent-support.html',
]
DRY = '--apply' not in sys.argv

CARD_RE = re.compile(r'<article class="svc-card reveal">(.*?)</article>', re.S)
GRID_RE = re.compile(r'<div class="svc-cards( wide)?">(.*?)</div>(?=<|\s*$)', re.S)
BLOCK_RE = re.compile(r'<(h3|h4|p|ul|ol)\b[^>]*>.*?</\1>', re.S)


def blocks_of(cardhtml):
    return [m.group(0) for m in BLOCK_RE.finditer(cardhtml)]


for page in PAGES:
    s = open(page, encoding='utf8').read()
    out, last, changed = [], 0, []
    for gm in GRID_RE.finditer(s):
        wide, body = gm.group(1) or '', gm.group(2)
        cards = CARD_RE.findall(body)
        if len(cards) < 2:
            continue
        counts = [len(blocks_of(c)) - 1 for c in cards]      # minus the h3
        others, lastn = counts[:-1], counts[-1]
        if lastn <= max(others):
            continue
        surplus = lastn - max(others)
        blks = blocks_of(cards[-1])
        tail = blks[-surplus:]
        if not all(t.startswith('<p') for t in tail):
            continue                                          # only pull plain paragraphs
        newlast = cards[-1]
        for t in tail:
            newlast = newlast.replace(t, '', 1)
        newcards = cards[:-1] + [newlast]
        grid = '<div class="svc-cards%s">%s</div>' % (
            wide, ''.join('<article class="svc-card reveal">%s</article>' % c for c in newcards))
        out.append((gm.start(), gm.end(), grid + ''.join(tail)))
        changed.append([html.unescape(re.sub('<[^>]+>', '', t))[:70] for t in tail])
    if changed:
        print(page)
        for c in changed:
            print('   pulled out of the last card:', c)
    if out and not DRY:
        for a, b, rep in reversed(out):
            s = s[:a] + rep + s[b:]
        open(page, 'w', encoding='utf8').write(s)
if DRY:
    print('\n(dry run; pass --apply to write)')
