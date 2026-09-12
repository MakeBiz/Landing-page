#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Английская версия /intdoc: разводим с makebiz.life теми же смыслами,
что и русскую (валюты, VAT, документы на двух языках, импорт и сроки).

    python3 .seo/uae/diverge_intdoc_en.py .
"""
import io, os, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.chdir(ROOT)
F = 'en/intdoc.html'

PAIRS = [
    ('<h1>The best supplier, <span class="grad">chosen for you</span></h1>',
     '<h1>Compare suppliers <span class="grad">across currencies</span> and justify the choice</h1>', 1),
    ('IntDoc extracts data from any supplier documents, compares offers by price, lead time and availability and shows the best one, with no manual work in Excel',
     'IntDoc pulls the data out of any quote, invoice or price list, brings dirhams, dollars and euros to one currency, puts VAT in its own column and shows whose offer is actually cheaper', 1),

    ('<h2>Supplier selection <span class="grad">takes up time and money</span></h2>',
     '<h2>In the UAE a supplier <span class="grad">is harder to compare than it looks</span></h2>', 1),
    ('Commercial proposals arrive in different formats, and you have to compare them manually. In this routine it is easy to miss the best terms',
     'Offers arrive in different formats, in different currencies and with different treatment of VAT. While all of that is reconciled by hand, the better deal slips away', 1),
    ('Quotes arrive in different formats: PDF, scans, emails', 'Quotes arrive as PDFs, scans and emails, some in English, some in Arabic', 1),
    ('Manual comparison in Excel takes hours', "Reconciling it in Excel eats the buyer's hours", 1),
    ('It is easy to miss the best terms', 'Prices in different currencies simply do not compare', 1),
    ('Errors when transferring data from documents', 'One supplier includes VAT, the next adds it on top', 1),
    ('No unified history of supplier comparisons', 'No single history of comparisons per supplier', 1),
    ('It is hard to justify a procurement decision', 'The decision is hard to explain to an auditor', 1),

    ('IntDoc recognizes the document line by line and extracts key fields, even from scans and phone photos',
     'IntDoc reads the document line by line and extracts the key fields even from a scan or a phone photo, in English and in Arabic', 1),
    ('>Price and currency<', '>Price, currency and the rate on the date<', 1),
    ('>Delivery time<', '>Lead time and shipping terms<', 1),
    ('>Stock availability<', '>Availability: local stock or import<', 1),
    ('>Payment terms<', '>Payment and 5% VAT<', 1),
    ('>Supplier details<', '>Supplier TRN and details<', 1),

    ('Quotes, invoices, price lists, PDF, scans and supplier photos', 'Quotes, invoices, price lists, PDFs, scans and photos from suppliers', 1),
    ('Price, lead time, availability, product range and terms from each document',
     'Price, currency, VAT, delivery time, availability and product range from each document', 1),
    ('Brings offers to a single format and compares suppliers',
     'Brings everything to one currency and one VAT basis, then compares', 1),
    ('The optimal offer with a justification for the choice',
     'The best offer with a justification you can show your director', 1),

    ('<h2>What <span class="grad">the procurement team</span> gets</h2>',
     '<h2>What <span class="grad">a procurement team in the UAE</span> gets</h2>', 1),
    ('Process incoming quotes faster', 'Work through incoming quotes faster', 1),
    ('Never miss the best terms', 'See the real price, not a number in someone else’s currency', 1),
    ('Less manual routine in Excel', 'Less manual reconciliation in Excel', 1),
    ('Transparency of supplier selection', 'It is clear why this supplier was chosen', 1),
    ('Accurate data on prices and terms', 'Accurate prices, rates and VAT on every line', 1),
    ('Fewer transfer errors from documents', 'Fewer mistakes when transferring from documents', 1),
    ('Savings on procurement', 'Savings on every purchase', 1),

    ('Extracts data from any documents', 'Reads any supplier document', 1),
    ('Compares by price, lead time and availability', 'Compares by price in one currency, delivery time and availability', 1),
    ('Finds the best offer with justification', 'Shows the best offer and explains why', 1),
    ('Eliminates manual transfer errors', 'Takes manual transfer errors out', 1),
    ('Copying data from different files', 'Copying data out of a dozen files', 1),
    ('Formats have to be reconciled by hand', 'Currencies and formats are reconciled by hand', 1),
    ('It is easy to make a mistake during transfer', 'It is easy to get the rate or the VAT wrong', 1),
    ('The best terms can slip away', 'The real saving is easy to miss', 1),

    ('Export of comparison results to CRM and Bitrix24', 'Comparison exported to CRM and Bitrix24', 1),
    ('Works with any supplier document format', 'Works with documents in English and Arabic', 1),

    ('The cost is calculated based on the number of suppliers and documents. We will start with a demo on your real quotes',
     'The price depends on the number of suppliers and documents. We start with a demo on your own quotes, in your own currencies', 1),
    ('Supplier comparison by basic fields, export to Excel', 'Comparison by basic fields with currencies converted, export to Excel', 1),

    ('Send a couple of real quotes, we will compare suppliers and show the best offer at the demo',
     'Send a couple of real quotes, we will bring the suppliers to one currency and show whose offer is better', 1),
    ('Hello! What do you compare most often: quotes, invoices, or price lists? I will show how IntDoc selects the best supplier.',
     'Hello! What do you compare most often: quotes, invoices or price lists? I will show how IntDoc brings them to one currency and picks the best supplier.', 1),
    ('Great, IntDoc will extract the price, delivery time and availability from these quotes and build a comparison table with the best offer. Will you send a couple of documents for the demo?',
     'Great, IntDoc will pull the price, currency, VAT, delivery time and availability out of those quotes and build one table with the best offer. Will you send a couple of documents for the demo?', 1),
    # второй проход 12 сен: добивка оставшихся совпадений
    ('Advanced fields and criteria, comparison history, export to CRM', 'Advanced fields and criteria, comparison history, export to Bitrix24', 1),
    ('For procurement departments with a regular flow of documents.', 'A procurement team with a steady flow of documents', 1),
    ('Comparison by price, delivery time and availability', 'Comparison by price in one currency and lead time', 1),
    ('Custom criteria, integrations and priority support', 'Your own criteria, integrations and priority support', 1),
    ('For large purchases, tenders, and high volumes.', 'Large purchases, tenders and high volumes', 1),
    ('For a first setup and a small flow of quotes.', 'A first setup and a small flow of quotes', 1),
    ('Storage of comparison and decision history', 'History of comparisons and decisions kept', 1),
    ('Quotes from suppliers, in PDF and scans', 'Supplier quotes in PDF and scans, some in Arabic', 1),
    ('Export of the comparison table to Excel', 'The comparison table exported to Excel', 1),
    ('Comparison history at your fingertips', 'The whole comparison history at hand', 1),
    ('IntDoc · Document AI for procurement', 'IntDoc · Document AI for buyers in the UAE', 1),
    ('Well-grounded procurement decisions', 'Procurement decisions that are easy to explain', 1),
    ('Comparison by the criteria you need', 'Comparison by your own criteria', 1),
    ('Exports the result to CRM and Excel', 'Hands the result to Bitrix24 and Excel', 1),
    ('Data extraction from any documents', 'Any supplier document parsed', 1),
    ('A single supplier comparison table', 'One table with every supplier on it', 1),
    ('into your procurement processes', 'into how you already buy', 1),
    ('Documents → supplier comparison', 'Documents → one currency, one table', 1),
    ('>No unified comparison history<', '>There is simply no comparison history<', 1),
    ('The best offer automatically', 'The best offer without manual checking', 1),
    ('Fast consolidation of offers', 'Every offer consolidated in minutes', 1),
    ('Export of comparison results', 'The finished comparison exported', 1),
    ('IntDoc vs manual comparison', 'IntDoc against reconciling by hand', 1),
    ('Discounts and special terms', 'Discounts and special conditions', 1),
    ('Less routine reconciliation', 'Less routine checking by hand', 1),
    ('What we compare most often', 'What buyers compare most often', 1),
    ('From a stack of documents', 'From a pile of supplier documents', 1),
    ('Audit trail for decisions', 'An audit trail behind every decision', 1),
    ('Stores comparison history', 'Keeps the comparison history', 1),
    ('for your document volume', 'for the volume you actually handle', 1),
    ('Scanning document fields', 'Reading the fields of a document', 1),
    ('Normalizes and compares', 'Brings to one currency and compares', 1),
    ('Nomenclature and items', 'Line items and product range', 1),
    ('IntDoc extracts fields', 'IntDoc pulls out the fields', 1),
    ('>any supplier documents<', '>supplier documents in two languages<', 1),
    ('Integrates seamlessly', 'Slots straight', 1),
]


def main():
    h = io.open(F, encoding='utf-8').read()
    before = h
    done = skipped = 0
    for old, new, n in PAIRS:
        assert old not in new, 'новая строка не должна содержать старую: %s' % old[:50]
        c = h.count(old)
        if c == 0:
            skipped += 1     # уже заменено
            continue
        if c != n:
            raise SystemExit('ожидалось %d вхождений, найдено %d: %s' % (n, c, old[:70]))
        h = h.replace(old, new)
        done += 1
    if h != before:
        io.open(F, 'w', encoding='utf-8').write(h)
    print('%s: заменено %d, уже было %d' % (F, done, skipped))


if __name__ == '__main__':
    main()
