import requests
from bs4 import BeautifulSoup
import csv
import re

URL = "https://www.poetryfoundation.org/poems/46473/if---"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')

quotes = []  # a list to store quotes

table = soup.find('div', attrs={'class': 'c-feature-bd'})
# print(table)
# print(quotes)

import unicodedata
def unicode_to_ascii(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def preprocess(w):
    w = unicode_to_ascii(w.lower().strip())
    w = re.sub(r"([?.!,¿])", r" \1 ", w)
    w = re.sub(r'[" "]+', " ", w)
    w = re.sub(r"newlinechar", "", w)
    w = re.sub(r"[^a-zA-Z?.!,¿]+", " ", w)
    w = w.rstrip().strip()

    return w

for i in table.findAllNext('div'):
    quote = {}
    string = i.text.split('\n')
    for j in string:
        strings = preprocess(j)
        if 'if ' in strings:
            quote['text'] = strings
            quotes.append(quote)

# for con in soup.find_all('div'):
#     print(con.text)
#     if ' if ' in con.text:
#         quotes.append(con.text)

print(quotes)


