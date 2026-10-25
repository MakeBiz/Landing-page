"""site.js makebiz.life -> site.js makebiztechnologies.com (RU): счётчик ОАЭ, AED, демо-данные под ОАЭ,
метка формы site-ae-*, без маяка /api/click (на этом сервере эндпоинта нет)"""
import sys, re
src, dst = sys.argv[1], sys.argv[2]
YM = '112503709'
s = open(src, encoding='utf-8').read()
R = [
 ("112151442", YM),
 ("  function goal(name) { try { if (window.ym) window.ym(112503709, 'reachGoal', name); } catch (e) {} try { if (window.gtag) window.gtag('event', name); } catch (e) {} }",
  "  var CONTACTS = { call: 1, telegram: 1, whatsapp: 1, max: 1, email: 1, tg_channel: 1 };\n"
  "  function goal(name) { try { if (window.ym) window.ym(112503709, 'reachGoal', name); } catch (e) {} try { if (window.gtag) { if (name === 'lead') window.gtag('event', 'generate_lead'); else if (CONTACTS[name]) window.gtag('event', 'contact_click', { method: name }); else window.gtag('event', name); } } catch (e) {} }"),
 ("    else if (/wa\\.me\\//i.test(h)) g = 'whatsapp';", "    else if (/wa\\.me\\//i.test(h)) g = 'whatsapp';\n    else if (/^mailto:/i.test(h)) g = 'email';"),
 ("function money() { return (Math.round(Math.random() * 90 + 10) * 1000).toLocaleString('ru-RU') + ' ₽'; }",
  "function money() { return 'AED ' + Math.round(Math.random() * 45 + 5) + 'K'; }"),
 ("['ООО «Вектор»', 'ТД «Север»', 'Логистик Плюс', 'СтройМаркет', 'Альфа Опт', 'ИП Смирнов', 'МедЦентр', 'АвтоДом', 'ФудТрейд', 'ПромСнаб'], S = ['WhatsApp', 'Сайт', 'Звонок', 'Telegram', 'Авито']",
  "['Al Noor', 'Gulf Logistics', 'Marina Realty', 'Emirates Build', 'Desert Foods', 'Smart Clinic', 'AutoHouse', 'Palm Supply', 'Creek Decor', 'Falcon Tech'], S = ['WhatsApp', 'Сайт', 'Звонок', 'Соцсети', 'Bayut']"),
 ("'Настроить обмен с 1С'", "'Настроить обмен с Zoho Books'"),
 ("'Добрый день! Стандартная настройка 97 500 ₽, расскажете о компании?'", "'Добрый день! Настройка CRM от 10 000 AED, расскажете о компании?'"),
 ("['in', 'ch-av', 'Авито', 'Объявление ещё актуально?']", "['in', 'ch-av', 'Соцсети', 'Апартаменты в Marina ещё свободны?']"),
 ("['in', 'ch-max', 'MAX', 'Можно созвониться завтра?']", "['in', 'ch-wa', 'WhatsApp', 'Можно созвониться завтра?']"),
 ("form: 'site-' + f.dataset.page, page: f.dataset.page, from: 'сайт makebiz.life'",
  "form: 'site-ae-' + f.dataset.page, page: f.dataset.page, from: 'сайт makebiztechnologies.com'"),
 ("    if (g === 'tg_channel' || g === 'cta_form' || /^\\/en(\\/|$)/.test(location.pathname)) return;\n", "    if (g === 'tg_channel' || g === 'cta_form') return;\n"),
 ("function fm(x){return Math.round(x).toLocaleString('ru-RU')+' ₽'}", "function fm(x){return Math.round(x).toLocaleString('ru-RU')+' AED'}"),
]
miss = [a[:60] for a, b in R if a not in s]
for a, b in R: s = s.replace(a, b)
open(dst, 'w', encoding='utf-8').write(s)
print('missing:', miss, '| ₽ left:', s.count('₽'), '| 112151442 left:', s.count('112151442'))
