# Помощники для SEO-правок сайта makebiztechnologies.com (правки head, шаблон бандла, JSON-LD)
import re, json, html

BASE = 'https://makebiztechnologies.com'

def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)

# ---------- JSON-строка шаблона бандла: декодирование с картой позиций ----------
def json_str_map(raw):
    assert raw[0] == '"' and raw[-1] == '"'
    out, pos = [], []
    i, n = 1, len(raw) - 1
    ESC = {'n': '\n', 't': '\t', 'r': '\r', 'b': '\b', 'f': '\f', '"': '"', '\\': '\\', '/': '/'}
    while i < n:
        c = raw[i]
        if c == '\\':
            e = raw[i + 1]
            if e == 'u':
                code = int(raw[i + 2:i + 6], 16); ln = 6
                if 0xD800 <= code <= 0xDBFF and raw[i + 6:i + 8] == '\\u':
                    low = int(raw[i + 8:i + 12], 16); ch = chr(0x10000 + ((code - 0xD800) << 10) + (low - 0xDC00)); ln = 12
                else:
                    ch = chr(code)
            else:
                ch = ESC[e]; ln = 2
            out.append(ch); pos.append(i); i += ln
        else:
            out.append(c); pos.append(i); i += 1
    pos.append(n)
    return ''.join(out), pos

def jenc(s):
    return json.dumps(s, ensure_ascii=False)[1:-1].replace('/', '\\u002F')

TPL_RE = re.compile(r'(<script type="__bundler/template">\s*)("(?:[^"\\]|\\.)*")(\s*</script>)', re.S)

def tpl_get(s):
    m = TPL_RE.search(s)
    return m

def tpl_patch(s, repl):
    """repl: список (старое, новое) в ДЕКОДИРОВАННОМ шаблоне; каждое старое должно встречаться ровно один раз"""
    m = tpl_get(s)
    if not m: raise ValueError('no bundler template')
    raw = m.group(2)
    dec, pos = json_str_map(raw)
    assert dec == json.loads(raw)
    spans = []
    expect = dec
    for old, new in repl:
        k = dec.find(old)
        if k < 0 or dec.find(old, k + 1) >= 0:
            raise ValueError('template: substring not unique/absent: %r' % old[:80])
        spans.append((pos[k], pos[k + len(old)], jenc(new)))
        expect = expect.replace(old, new, 1)
    spans.sort(reverse=True)
    new_raw = raw
    for a, b, enc in spans:
        new_raw = new_raw[:a] + enc + new_raw[b:]
    assert json.loads(new_raw) == expect, 'template patch verification failed'
    return s[:m.start(2)] + new_raw + s[m.end(2):]

def tpl_decoded(s):
    m = tpl_get(s)
    return json.loads(m.group(2)) if m else None

# ---------- head-правки над строкой HTML (для внешнего документа и для шаблона) ----------
def head_bounds(h):
    a = h.find('<head'); a = h.find('>', a) + 1; b = h.find('</head>')
    return a, b

def esc_attr(v): return html.escape(v, quote=True)

def set_title(h, title):
    a, b = head_bounds(h)
    head = h[a:b]
    new_head, n = re.subn(r'<title>.*?</title>', '<title>' + html.escape(title, quote=False) + '</title>', head, count=1, flags=re.S)
    if not n: new_head = '<title>' + html.escape(title, quote=False) + '</title>\n' + head
    return h[:a] + new_head + h[b:]

def set_meta(h, key, value, attr='name'):
    a, b = head_bounds(h)
    head = h[a:b]
    pat = re.compile(r'<meta\s+' + attr + r'="' + re.escape(key) + r'"\s+content="[^"]*"\s*/?>')
    tag = '<meta ' + attr + '="' + key + '" content="' + esc_attr(value) + '">'
    ms = list(pat.finditer(head))
    if ms:
        head = head[:ms[0].start()] + tag + pat.sub('', head[ms[0].end():])
    else:
        head = head.rstrip() + '\n  ' + tag + '\n'
    return h[:a] + head + h[b:]

def get_meta(h, key, attr='name'):
    m = re.search(r'<meta\s+' + attr + r'="' + re.escape(key) + r'"\s+content="([^"]*)"', h[:h.find('</head>')])
    return html.unescape(m.group(1)) if m else None

LD_RE = re.compile(r'(?:<!--mb-ld-->)?<script type="application/ld\+json"[^>]*>.*?</script>(?:<!--/mb-ld-->)?\s*', re.S)

def get_lds(h):
    a, b = head_bounds(h)
    return [json.loads(x) for x in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', h[a:b], re.S)]

def replace_lds(h, objs, marker_after=None):
    """убирает все JSON-LD из head и ставит новые одним блоком (после <meta charset> или в начало head)"""
    a, b = head_bounds(h)
    head = LD_RE.sub('', h[a:b])
    block = '<!--mb-ld-->' + ''.join('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False, separators=(',', ':')) + '</script>' for o in objs) + '<!--/mb-ld-->\n'
    m = re.search(r'<meta charset="utf-8">\s*', head, re.I)
    if m: head = head[:m.end()] + block + head[m.end():]
    else: head = '\n' + block + head
    return h[:a] + head + h[b:]

def set_canonical(h, url):
    a, b = head_bounds(h); head = h[a:b]
    tag = '<link rel="canonical" href="' + esc_attr(url) + '">'
    if re.search(r'<link rel="canonical"[^>]*>', head): head = re.sub(r'<link rel="canonical"[^>]*>', tag, head, count=1)
    else: head = head.rstrip() + '\n  ' + tag + '\n'
    return h[:a] + head + h[b:]

def set_hreflang(h, pairs):
    """pairs: [(hreflang, url), ...]; заменяет все alternate hreflang в head"""
    a, b = head_bounds(h); head = h[a:b]
    head = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*"\s*/?>', '', head)
    tags = ''.join('\n  <link rel="alternate" hreflang="%s" href="%s">' % (l, esc_attr(u)) for l, u in pairs)
    m = re.search(r'<link rel="canonical"[^>]*>', head)
    if m: head = head[:m.end()] + tags + head[m.end():]
    else: head = head.rstrip() + tags + '\n'
    return h[:a] + head + h[b:]

def ld_script(obj, id_=None):
    return '<script type="application/ld+json"' + (' id="%s"' % id_ if id_ else '') + '>' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>'
