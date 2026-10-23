import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
o = "  let top = part('top.html');\n"
n = ("  let top = part('top.html');\n"
     "  if (!/(^|\\/)news/.test(rel)) top = top.replace('nav-link is-active', 'nav-link');\n"
     "  if (/(^|\\/)bitrix-/.test(rel)) top = top.replace('<div class=\"nav-dd\">', '<div class=\"nav-dd is-active\">');\n")
assert s.count(o) == 1; s = s.replace(o, n); open(p, 'w', encoding='utf-8').write(s); print('ok')
