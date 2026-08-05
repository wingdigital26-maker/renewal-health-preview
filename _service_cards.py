"""Service-page restructure:
   - lift the orphan kicker <h2> into an .eyebrow above the real first <h2>
   - promote orphan heading-like <p> blocks to real headings (no words lost)
   - turn runs of sibling <h3> sections into scannable card grids
   - programs-packages: 01/02/03 blocks become big package cards
   - a small set of explicit, logged de-duplications
Only structure changes here except the explicit DEDUPE list, which is logged
point by point in SERVICES-MERGE-LOG.md.
"""
import re, sys, html

PAGES = [
    'services.html', 'naturopathic-detox.html', 'gut-health-support.html',
    'weight-metabolic-health.html', 'hormone-balance-support.html',
    'inflammation-support.html', 'emotional-overwhelm-nervous-system.html',
    'neurodivergent-support.html', 'programs-packages.html',
]

BLOCK_RE = re.compile(r'<(h2|h3|h4|p|ul|ol|figure|div|blockquote|a)\b[^>]*>', re.I)


def tokenize(inner):
    """Split the flow's inner HTML into top-level blocks."""
    blocks, i = [], 0
    while i < len(inner):
        m = BLOCK_RE.search(inner, i)
        if not m:
            tail = inner[i:]
            if tail.strip():
                blocks.append(('raw', tail))
            break
        if inner[i:m.start()].strip():
            blocks.append(('raw', inner[i:m.start()]))
        tag = m.group(1).lower()
        # find the matching close tag, allowing nesting of the same tag
        depth, pos = 1, m.end()
        open_re = re.compile(r'<%s\b' % tag, re.I)
        close_re = re.compile(r'</%s\s*>' % tag, re.I)
        while depth:
            no, nc = open_re.search(inner, pos), close_re.search(inner, pos)
            if not nc:
                raise ValueError('unclosed <%s>' % tag)
            if no and no.start() < nc.start():
                depth += 1
                pos = no.end()
            else:
                depth -= 1
                pos = nc.end()
        blocks.append((tag, inner[m.start():pos]))
        i = pos
    return blocks


def text_of(blk):
    return html.unescape(re.sub(r'<[^>]+>', '', blk[1])).strip()


def inner_of(blk):
    return re.sub(r'^<[^>]+>|</[a-zA-Z0-9]+>\s*$', '', blk[1].strip())


# ---------------------------------------------------------------- de-duplication
# Each entry: (page, kind, exact visible text). Justified in SERVICES-MERGE-LOG.md.
DROP_BLOCKS = {
    'naturopathic-detox.html': [
        'A Gentle, Root-Cause Approach to Detoxification',
        'Supporting Detox at a System-Wide Level',
    ],
    'services.html': [
        'A Gentle, Root-Cause Approach to Detoxification',
        'Supporting Detox at a System-Wide Level',
    ],
    'weight-metabolic-health.html': [
        # the SECOND, verbatim-duplicate h3 label; its body text is kept and
        # merged under the single remaining heading of the same name
        ('h3', 'How Hormones Affect Weight and Metabolism', 2),
    ],
}

# Whole runs removed because they are byte-for-byte duplicates of another page.
DROP_RUNS = {
    'inflammation-support.html': [
        # the detox page's kicker, verbatim
        ('h2', 'Gentle Root-Cause Detox Support', 'h2', 'Gentle Root-Cause Detox Support'),
        # the detox page's system-wide detox section, verbatim, three h3 blocks
        ('h2', 'How Gentle, System-Wide Detox Support Works',
         'h3', 'How Inflammation Affects Your Whole-Body Health'),
    ],
}

# heading-like orphan paragraphs -> real headings (identical words)
PROMOTE = {
    'naturopathic-detox.html': {
        'Is Naturopathic and Homeopathic Detox Right for You?': ('h3', 'Is Naturopathic Detox Right for You?'),
    },
    'services.html': {
        'Is Naturopathic and Homeopathic Detox Right for You?': ('h3', 'Is Naturopathic Detox Right for You?'),
    },
    'gut-health-support.html': {
        'Is This Gut Health Approach Right for You?': ('h3', None),
    },
    'weight-metabolic-health.html': {
        'This Weight and Metabolic Approach Right for You?': ('h3', None),
    },
    'inflammation-support.html': {
        'Is This Inflammation Support Approach Right for You?': ('h3', None),
    },
    'emotional-overwhelm-nervous-system.html': {
        'Is Emotional Overwhelm Support Right for You?': ('h3', None),
    },
    'neurodivergent-support.html': {
        'Is Neurodivergent Support Approach Right for You?': ('h3', None),
    },
    'hormone-balance-support.html': {
        'Is This Hormone Balance Approach Right for You?': ('h3', None),
    },
}

REPORT = []


def restructure(page, inner):
    blocks = tokenize(inner)
    log = []

    # --- 1. drop whole duplicated runs -----------------------------------
    for start_tag, start_txt, end_tag, end_txt in DROP_RUNS.get(page, []):
        si = next((i for i, b in enumerate(blocks)
                   if b[0] == start_tag and text_of(b) == start_txt), None)
        if si is None:
            continue
        if end_tag == start_tag and end_txt == start_txt:
            ei = si + 1
        else:
            ei = next(i for i in range(si + 1, len(blocks))
                      if blocks[i][0] == end_tag and text_of(blocks[i]) == end_txt)
        removed = [text_of(b)[:60] for b in blocks[si:ei] if b[0] in ('h2', 'h3', 'h4')]
        log.append('removed duplicated run starting "%s" (headings: %s)' % (start_txt, removed))
        blocks = blocks[:si] + blocks[ei:]

    # --- 2. drop individual duplicated blocks ----------------------------
    for spec in DROP_BLOCKS.get(page, []):
        if isinstance(spec, str):
            idx = next((i for i, b in enumerate(blocks)
                        if b[0] == 'p' and text_of(b) == spec), None)
            if idx is not None:
                log.append('removed duplicate line "%s"' % spec)
                blocks.pop(idx)
        else:
            tag, txt, nth = spec
            hits = [i for i, b in enumerate(blocks) if b[0] == tag and text_of(b) == txt]
            if len(hits) >= nth:
                log.append('removed duplicate <%s> "%s" (occurrence %d of %d)'
                           % (tag, txt, nth, len(hits)))
                blocks.pop(hits[nth - 1])

    # --- 3. promote orphan heading-like paragraphs -----------------------
    for i, b in enumerate(blocks):
        if b[0] != 'p':
            continue
        rule = PROMOTE.get(page, {}).get(text_of(b))
        if rule:
            tag, newtext = rule
            body = newtext if newtext else inner_of(b)
            if newtext:
                log.append('retitled "%s" -> "%s" (dual naturopathic/homeopathic naming dropped)'
                           % (text_of(b), newtext))
            blocks[i] = (tag, '<%s class="reveal">%s</%s>' % (tag, body, tag))

    # --- 4. kicker: first <h2> immediately followed by another <h2> ------
    for i, b in enumerate(blocks):
        if b[0] == 'h2':
            if i + 1 < len(blocks) and blocks[i + 1][0] == 'h2':
                blocks[i] = ('p', '<p class="eyebrow reveal">%s</p>' % inner_of(b))
                log.append('kicker "%s" restyled as an eyebrow on the heading below '
                           '(same words, no longer a second stacked H2)' % text_of(b))
            break

    # --- 5. programs packages: 01/02/03 -> big package cards -------------
    if page == 'programs-packages.html':
        out, i = [], 0
        while i < len(blocks):
            b = blocks[i]
            m = re.match(r'^(\d+)\s*\|\s*(.+)$', text_of(b)) if b[0] == 'h2' else None
            if m:
                j = i + 1
                while j < len(blocks) and blocks[j][0] != 'h2':
                    j += 1
                num, name = m.group(1), m.group(2)
                body = ''.join(x[1] for x in blocks[i + 1:j])
                out.append(('div',
                            '<article class="pkg-card reveal">'
                            '<span class="pkg-num" aria-hidden="true">%s</span>'
                            '<h2 class="pkg-title"><span class="pkg-num-sr">%s |</span> %s</h2>'
                            '%s</article>' % (num, num, name, body)))
                log.append('package "%s | %s" wrapped as a card (content verbatim)' % (num, name))
                i = j
                continue
            out.append(b)
            i += 1
        # group consecutive package cards into a grid
        blocks, i = [], 0
        while i < len(out):
            if out[i][0] == 'div' and 'pkg-card' in out[i][1]:
                j = i
                while j < len(out) and out[j][0] == 'div' and 'pkg-card' in out[j][1]:
                    j += 1
                blocks.append(('div', '<div class="pkg-cards">%s</div>'
                               % ''.join(x[1] for x in out[i:j])))
                i = j
            else:
                blocks.append(out[i])
                i += 1

    # --- 6. runs of sibling <h3> sections -> card grids ------------------
    out, i = [], 0
    while i < len(blocks):
        if blocks[i][0] == 'h3':
            groups, j = [], i
            while j < len(blocks) and blocks[j][0] == 'h3':
                k = j + 1
                while k < len(blocks) and blocks[k][0] in ('p', 'ul', 'ol', 'h4'):
                    k += 1
                groups.append((j, k))
                j = k
            if len(groups) >= 2:
                cards, sizes = [], []
                for (a, b) in groups:
                    head = re.sub(r'^<h3', '<h3', blocks[a][1])
                    body = ''.join(x[1] for x in blocks[a + 1:b])
                    sizes.append(b - a - 1 + sum(1 for x in blocks[a + 1:b] if x[0] in ('ul', 'ol')) * 2)
                    cards.append('<article class="svc-card reveal">%s%s</article>' % (head, body))
                wide = ' wide' if max(sizes) > 2 else ''
                out.append(('div', '<div class="svc-cards%s">%s</div>' % (wide, ''.join(cards))))
                log.append('%d sibling sections turned into a %s card grid: %s'
                           % (len(groups), 'wide' if wide else 'compact',
                              [text_of(blocks[a])[:44] for a, _ in groups]))
                i = j
                continue
        out.append(blocks[i])
        i += 1
    blocks = out

    REPORT.append((page, log))
    return ''.join(b[1] for b in blocks)


def run():
    for page in PAGES:
        s = open(page, encoding='utf8').read()
        m = re.search(r'(<section class="section intro-reveal article[^"]*"><div class="inner narrow flow">\n?)(.*?)(\n?</div></section>)', s, re.S)
        if not m:
            print('!! no article flow in', page)
            continue
        new = restructure(page, m.group(2))
        s = s[:m.start(2)] + new + s[m.end(2):]
        open(page, 'w', encoding='utf8').write(s)
    for page, log in REPORT:
        print('\n== ' + page)
        for line in log:
            print('   - ' + line)


if __name__ == '__main__':
    run()
