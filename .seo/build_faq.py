# -*- coding: utf-8 -*-
# Добавляет разметку FAQPage в mb-ld и подключает /mb-faq.js на нужных страницах.
import io, os, re, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from faq_data import FAQ, FAQ_EN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://makebiztechnologies.com'
URL = {'index.html': '/', 'en/index.html': '/en'}

def page_url(rel):
    if rel in URL: return SITE + URL[rel]
    return SITE + '/' + rel[:-len('.html')]

def apply(rel, qa):
    p = os.path.join(ROOT, *rel.split('/'))
    s = io.open(p, encoding='utf-8').read()
    url = page_url(rel)
    node = {"@type": "FAQPage", "@id": url + "#faq", "url": url,
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}
    m = re.search(r'(<!--mb-ld--><script type="application/ld\+json">)([\s\S]*?)(</script><!--/mb-ld-->)', s)
    if not m:
        return rel, 'нет блока mb-ld'
    d = json.loads(m.group(2))
    g = d.get('@graph') or [d]
    g = [n for n in g if n.get('@type') != 'FAQPage'] + [node]
    d['@graph'] = g
    s = s[:m.start()] + m.group(1) + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + m.group(3) + s[m.end():]
    tag = '<script src="/mb-faq.js" defer></script>'
    if 'mb-faq.js' not in s:
        s = s.replace('<!--/mb-attr-->', '<!--/mb-attr-->\n' + tag, 1)
    io.open(p, 'w', encoding='utf-8').write(s)
    return rel, 'ok, вопросов %d' % len(qa)

for rel, qa in list(FAQ.items()) + list(FAQ_EN.items()):
    print('%-24s %s' % apply(rel, qa))
