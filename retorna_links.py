'''
Este programa cria automaticamente na mesma pasta
o arquivo excel com os links presentes na url inserida

Instalar:
pandas
requests
beautifulSoup4
xlwt
'''

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def getArrayLinks(url):
    '''
    Retorna 2 arrays, o primeiro com todos os links presentes na URL
    e o segundo com o horário da pesquisa
    Qualquer 'href' que não possuir 'https' ou 'http' será 
    desconsiderado
    '''
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, 'html.parser')

    array_links = []
    array_time = []
    for a in soup.find_all('a'):
        if 'https://' in str(a.get('href')) or 'http://' in str(a.get('href')):
            if a.get('href') not in array_links:
                array_links.append(a.get('href'))
                array_time.append(datetime.now().time())

    return array_links, array_time


def getLinks(url, depth, fileName):
    '''
    Depth - profundidade da pesquisa:
        0 - Retorna somente os links presentes na url
        1 - Retorna os anteriores e o links presentes em cada url encontrada
        2 - Todos os anteriores mais os links das novas urls
        .
        .
        .

    Utilizar o Depth a partir de 2 torna o programa muito lento

    fileName: nome do arquivo excel que será gerado
    '''
    array_links, array_time = getArrayLinks(url)
    
    while depth > 0:
        count = 1
        array_links_temp = []
        array_time_temp = []

        if count == 1:
            array_new_links = array_links

        # Retorna os novos links a partir dos links anteriores
        for link in array_new_links:
            depth_array_links, depth_array_time = getArrayLinks(link)

            array_links_temp += depth_array_links
            array_time_temp += depth_array_time

        array_new_links = []

        # Verifica se o link já foi listado:
        for i, link in enumerate(array_links_temp):
            if link not in array_links:
                array_links.append(link)
                array_new_links.append(link) # Somente os novos links passarão na próxima iteração
                array_time.append(array_time_temp[i])

        depth -= 1
        count += 1

    dict_all_links= {'links': array_links, 'atualTime': array_time}
    dados = pd.DataFrame(data = dict_all_links)
    dados.to_excel(fileName)


getLinks('https://www.facebook.com/', 0, 'linksFb.xls')