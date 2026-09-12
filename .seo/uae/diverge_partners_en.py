#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Английская версия /partners: разводим с makebiz.life той же рамкой.

    python3 .seo/uae/diverge_partners_en.py .
"""
import io, os, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.chdir(ROOT)
F = 'en/partners.html'

PAIRS = [
    ('MakeBiz Partner Program', 'The MakeBiz partner programme in the UAE'),
    ('Bring in business and <span style="color:#16C15A">earn from every payment</span>',
     'Introduce us to business in the UAE and <span style="color:#16C15A">earn from every payment</span>'),
    ('You recommend, we take on the meetings, implementation, and support. You get 20% from the first deal and 10% from all client payments for another year',
     'You make the introduction, we run the meetings, the implementation and the support. You get 20% of the first payment and 10% of every client payment for another year, in dirhams'),
    ('Estimate. 20% from the first client payment and 10% from all subsequent payments for another year. On average a client pays 4 times a year, and a repeat payment is about 50% of the first',
     'Estimate. 20% of the first client payment and 10% of everything after that for another year. On average a client pays four times a year, and a repeat payment is about half the first'),

    ('From recommendation to your payout', 'From the introduction to your payout'),
    ('You bring in a client in any convenient way, and we take care of everything else. Every lead is assigned to you automatically',
     'You bring the client in whatever way suits you, the rest is on us. Every lead is assigned to you automatically'),
    ('Share a link or a contact', 'Share a link or introduce us in person'),
    ('In the channel, on social media, on the website, or in person, whichever suits you best',
     'In your channel, on social media, on your site or over coffee, whichever suits you'),
    ('The lead is assigned to you', 'The lead is yours straight away'),
    ('The request is automatically linked to you, without spreadsheets or disputes',
     'The link is made automatically, with no spreadsheets and no arguments'),
    ('We close the deal and implement', 'We run the deal and the implementation'),
    ('Meetings, proposal, launch and support on our side', 'Meetings, proposal, launch and support are our part'),
    ('You receive a payout', 'You get paid'),
    ('We accrue on actual client payment, with withdrawal in the way that suits you',
     'We credit it the day the client pays, and you withdraw the way that suits you'),

    ('20% upfront and 10% for the entire following year', '20% upfront and another 10% for the whole following year'),
    ('This is not a one-time commission but income that grows with every client payment. One good contact supports you for 12 months',
     'This is not a one-off commission but income that grows with every client payment. One good contact feeds you all year'),
    ('>From the first deal<', '>From the first payment<'),
    ('We credit 20% after the first client payment', 'We credit 20% once the client has paid'),
    ('From all subsequent payments', 'From every payment after that'),
    ('Another 10% from every payment of this client for a year, subscriptions, support, improvements',
     'Another 10% of every payment from that client for a year: subscriptions, support, improvements'),
    ('Adds up across all clients', 'It adds up across all your clients'),
    ('The more you refer, the higher your cumulative monthly income', 'The more you introduce, the higher your cumulative income each month'),

    ('Revenue, leads, and operations are visible in real time', 'Revenue, leads and operations are visible in real time'),
    ('Everything in your personal account, transparent and without manual recalculation',
     'Everything in your account, with no manual recalculation and no chasing'),
    ('Cumulatively across all your clients', 'Cumulatively across every client you brought'),
    ('Every lead and payout in plain sight', 'Every lead and every payout in plain sight'),

    ('A convenient dashboard with statistics', 'A dashboard with the numbers at hand'),
    ('You log in and see everything: how many you brought, what is in progress, what is due for payout and when. Transparent for every lead and every transaction',
     'You log in and see it all: how many you brought, what is in progress, what is due and when. Clear on every single lead'),
    ('Deals by month, conversion, earned and amount to be paid out', 'Deals by month, conversion, earnings and the amount due'),
    ('Transparency of leads and operations', 'Leads and operations in the clear'),
    ('The status of every deal and calculation of the commission for every payment',
     'The status of each deal and the commission worked out on every payment'),
    ('Grow from Bronze to Gold and unlock bonuses for activity', 'You move from Bronze to Gold, and bonuses open up as you go'),
]


def main():
    h = io.open(F, encoding='utf-8').read()
    before = h
    done = skipped = 0
    for old, new in PAIRS:
        assert old not in new, 'новая строка не должна содержать старую: %s' % old[:50]
        if old not in h:
            skipped += 1
            continue
        h = h.replace(old, new)
        done += 1
    if h != before:
        io.open(F, 'w', encoding='utf-8').write(h)
    print('%s: заменено %d, уже было %d' % (F, done, skipped))


if __name__ == '__main__':
    main()
