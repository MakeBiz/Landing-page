# соответствие RU-адресов английским на makebiztechnologies.com
EN_SLUG = {'/bitrix-korobka': '/bitrix-on-premise', '/bi-analitika': '/bi-analytics', '/keysy': '/cases', '/ceny': '/pricing', '/o-kompanii': '/about'}
def en_path(p):
    if p == '/': return '/en'
    for k, v in EN_SLUG.items():
        if p == k or p.startswith(k + '/'): return '/en' + v + p[len(k):]
    return '/en' + p
