import requests
from bs4 import BeautifulSoup
import csv
import re
import unicodedata

with open(r'C:\Users\HARSHAVARDHAN A\PycharmProjects\TsecHacks\urls.txt', 'r') as links:
    str = links.read()
    links_list = str.split('\n')

URL = "https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=south-park"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')

text_lists = []

table = soup.find('div', attrs={'class': 'main-content'})
# for i in soup.find_all(['p', 'li']):
for i in table.findAllNext('a'):
    print(i['href'])
    # string = i.text.split('.')
    # for j in string:
    #     text_dict = {}
    #     strings = preprocess(j)
    #     if 'if ' in strings or 'else ' in strings:
    #         text_dict['text'] = strings
    #         text_lists.append(text_dict)


print(text_lists)
print(len(text_lists))

# f = open(r'C:\Users\HARSHAVARDHAN A\PycharmProjects\TsecHacks\newURLS.txt', 'a', newline='\n')
# print('debug')
# writer = csv.DictWriter(f, fieldnames=['text'])
# writer.writerows()
# f.close()
