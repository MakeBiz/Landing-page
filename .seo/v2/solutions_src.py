"""Список страниц-решений из конвейера (.seo/uae/link_solutions.py, словарь T): карточки для блока на /bitrix"""
import os, ast
SKIP = {'/bitrix-whatsapp', '/bitrix-accounting'}  # на новом сайте это /bitrix-messengers и /bitrix-integrations
def solutions(lang):
    site = os.environ.get('MB_SITE', '')
    f = os.path.join(site, '.seo', 'uae', 'link_solutions.py')
    try:
        src = open(f, encoding='utf-8').read()
    except OSError:
        return []
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') == 'T':
            T = ast.literal_eval(node.value)
            return [(e, t, d, u) for e, t, d, u in T[lang][4] if u not in SKIP]
    return []
