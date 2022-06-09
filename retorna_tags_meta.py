'''
Instalar:
BeautifulSoup4
Requests
'''

import requests
from bs4 import BeautifulSoup
import json


def getMetas(url):
    '''
    Retora um Json com todas as tags <meta>
    presentes no html
    '''
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, 'html.parser')
    array_tags_meta = {}
    for i, meta in enumerate(soup.find_all('meta')):
        array_tags_meta[i] = (str(meta))

    return json.dumps(array_tags_meta)


res = getMetas('https://www.facebook.com/')
print(res)