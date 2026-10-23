"""site-en.js для makebiztechnologies.com из site-ae.js (RU ОАЭ): английские демо-тексты, метка формы site-ae-en-*"""
import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
R = [
 ("'Отправляем...'", "'Sending...'"), ("'Отправить заявку'", "'Send request'"),
 ("form: 'site-ae-' + f.dataset.page, page: f.dataset.page, from: 'сайт makebiztechnologies.com'", "form: 'site-ae-' + f.dataset.page, page: f.dataset.page, from: 'makebiztechnologies.com EN'"),
 ("'Телефон'", "'Phone'"), ("'ru-RU'", "'en-US'"),
 ("S = ['WhatsApp', 'Сайт', 'Звонок', 'Соцсети', 'Bayut']", "S = ['WhatsApp', 'Website', 'Call', 'Social', 'Bayut']"),
 ("'Соцсети'", "'Social'"),
 ("['Не создаются сделки из формы', 'Настроить обмен с Zoho Books', 'Обучить новый отдел', 'Доработать воронку', 'Права доступа для склада', 'Робот не ставит задачу', 'Подключить телефонию', 'Новые поля в карточке']",
  "['Form does not create deals', 'Set up Zoho Books exchange', 'Train a new department', 'Adjust the pipeline', 'Warehouse access rights', 'Automation does not set a task', 'Connect telephony', 'New fields in the card']"),
 ("'<span class=\"ico\">Б24</span>", "'<span class=\"ico\">B24</span>"), ("'</b><small>заявка №'", "'</b><small>request No. '"),
 ("'Новая'", "'New'"), ("'В работе'", "'In progress'"), ("'Решено'", "'Solved'"),
 ("'Здравствуйте, сколько стоит настройка CRM?'", "'Hello, how much is a CRM setup?'"), ("'Менеджер, из Битрикс24'", "'Manager, from Bitrix24'"),
 ("'Добрый день! Настройка CRM от 10 000 AED, расскажете о компании?'", "'Good afternoon! CRM setup starts from AED 10,000, could you tell us about the company?'"),
 ("'Пришлите КП, пожалуйста'", "'Please send a quote'"), ("'ИИ-агент'", "'AI agent'"), ("'КП отправлено, сделка переведена на этап «КП»'", "'Quote sent, deal moved to the Quote stage'"),
 ("'Апартаменты в Marina ещё свободны?'", "'Is the Marina apartment still available?'"), ("'Можно созвониться завтра?'", "'Can we call tomorrow?'"),
 ("[['С', 'Связной', 'Ответил клиенту в WhatsApp за 12 сек'], ['Ф', 'Финансист', 'Остатки по счетам обновлены'], ['А', 'Аналитик', 'Разобрал 48 звонков, 3 требуют внимания'], ['З', 'Закупщик', 'Собрал 6 прайсов, лучший на 8% дешевле'], ['К', 'Квалификатор', 'Горячий лид передан менеджеру'], ['Н', 'Наймщик', 'Кандидат прошёл тест, приглашение отправлено']]",
  "[['L', 'Liaison', 'Replied to a client in WhatsApp in 12 sec'], ['F', 'Finance', 'Account balances updated'], ['A', 'Analyst', 'Reviewed 48 calls, 3 need attention'], ['P', 'Procurement', 'Collected 6 price lists, best is 8% cheaper'], ['Q', 'Qualifier', 'Hot lead passed to a manager'], ['H', 'Recruiter', 'Candidate passed the test, invitation sent']]"),
 ("'</small></span><span class=\"st ok\">готово</span>'", "'</small></span><span class=\"st ok\">done</span>'"),
 ("'Видео MakeBiz'", "'MakeBiz video'"),
 ("function fm(x){return Math.round(x).toLocaleString('en-US')+' AED'}", "function fm(x){return 'AED '+Math.round(x).toLocaleString('en-US')}"),
]
miss = [a[:70] for a, b in R if a not in s]
for a, b in R: s = s.replace(a, b)
open(dst, 'w', encoding='utf-8').write(s)
left = [l.strip()[:120] for l in s.split('\n') if re.search('[А-Яа-я]', l) and not l.strip().startswith('//')]
print('missing:', miss); print('cyrillic left:', left)
