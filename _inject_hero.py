import re
frag = open('_hero_entrance.part', encoding='utf8').read().strip()
START = '<!-- hero entrance:'
END = '</svg>'
for f in ('index.html', 'home.html'):
    s = open(f, encoding='utf8').read()
    # remove any legacy photo dragonfly
    s = re.sub(r'\n?[ \t]*<img class="df-flight"[^>]*>\n?', '\n', s)
    # replace an existing entrance block, else insert after <body>
    i = s.find(START)
    if i != -1:
        j = s.index(END, i) + len(END)
        s = s[:i] + frag + s[j:]
    else:
        marker = '<body class="has-hero">\n'
        assert marker in s, f + ': body tag not matched'
        s = s.replace(marker, marker + frag + '\n', 1)
    open(f, 'w', encoding='utf8').write(s)
    print('ok', f)
