# robots.txt: больше AI-ботов в явном списке (build_d.py и сам robots.txt одинаково)
import sys, os
D = sys.argv[1]
o = "User-agent: YandexAdditional\nUser-agent: YandexAdditionalBot\nAllow: /"
n = ("User-agent: YandexAdditional\nUser-agent: YandexAdditionalBot\nUser-agent: anthropic-ai\nUser-agent: GoogleOther\nUser-agent: Bingbot\n"
     "User-agent: DuckAssistBot\nUser-agent: MistralAI-User\nUser-agent: Amazonbot\nUser-agent: cohere-ai\nUser-agent: meta-externalagent\nAllow: /")
for f in ('.seo/build_d.py', 'robots.txt'):
    p = os.path.join(D, f); s = open(p, encoding='utf-8').read()
    if 'User-agent: anthropic-ai' in s: print(f, 'already'); continue
    assert s.count(o) == 1, f; s = s.replace(o, n); open(p, 'w', encoding='utf-8').write(s); print(f, 'ok')
