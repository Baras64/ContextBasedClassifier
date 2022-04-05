import requests
from bs4 import BeautifulSoup
import csv
import re
import unicodedata

links_list = []

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
with open(r'C:\Users\HARSHAVARDHAN A\PycharmProjects\TsecHacks\newURLS.txt', 'r') as links:
    str = links.read()
    links_list = str.split('\n')
count = 1
for lonks in links_list:
    print(count)
    gglinks = "https://www.springfieldspringfield.co.uk/"+lonks
    URL = gglinks
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')

    text_lists = []

    table = soup.find('div', attrs={'class': 'wrapper'})
    # for i in soup.find_all(['p', 'li']):
    for i in table.findAllNext('div', attrs={'class': 'scrolling-script-container'}):
        string = i.text.split('.')
        for j in string:
            text_dict = {}
            strings = preprocess(j)
            if 'if ' in strings or 'else ' in strings:
                text_dict['text'] = strings
                text_lists.append(text_dict)


    print(text_lists)
    print(len(text_lists))

    f = open(r'C:\Users\HARSHAVARDHAN A\PycharmProjects\TsecHacks\literature_harsh.csv', 'a', newline='\n')
    print('debug')
    writer = csv.DictWriter(f, fieldnames=['text'])
    writer.writerows(text_lists)
    f.close()
    count+=1





