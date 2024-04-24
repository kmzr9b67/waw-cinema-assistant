from pprint import pprint

import requests
from bs4 import BeautifulSoup
cinema = {}

def amondo():
    url = 'https://kinoamondo.pl/repertuar/'
    soup = requests.get(url).text
    soup = BeautifulSoup(soup, 'html.parser')
    soup = soup.find(id='schedule-2024-04-24')
    title = soup.find_all(class_ ='no-underline')
    title = [i.text for i in title]
    time = soup.find_all(class_ = 'time')
    time = [i.text for i in time]
    wynik = result(title,time, 'AMONDO')
    return wynik
def iluzjon():
    url = 'https://www.iluzjon.fn.org.pl/repertuar.html'
    soup = requests.get(url).text
    soup = BeautifulSoup(soup, 'html.parser')
    soup = soup.find(class_='box wide')
    soup = soup.table
    time_and_hour = soup.find_all(class_ = 'hour')
    time_and_hour = [i.text.split(' - ') for i in time_and_hour]
    time = []
    title = []
    for i in range(0, len(time_and_hour)):
        time.append(time_and_hour[i][0])
        title.append(time_and_hour[i][1])
    wynik = result(title, time, 'ILUZJON')
    return wynik

def result(title, time, kino):
    for i in range(0, len(title), 1):
        help_l={}
        help_l['title'] = title[i]
        help_l['time'] = time[i]
        help_l['cinema'] = kino
        help_l['reating'] = 'N/A'
        cinema[title[i]] = help_l
    return cinema

def merge(dic_1, dic_2):
    for i in dic_1:
        for j in dic_2:
            if i == j:
                help_l = {}
                help_l['title'] = dic_1[i]['title']
                help_l['time'] = dic_1[i]['time']
                help_l['cinema'] = f'{dic_1[i]['cinema']} & {dic_2[j]['cinema']}'
                help_l['reating'] = 'N/A'
                cinema[dic_1[i]['title']] = help_l

    updated = {**dic_1, **dic_2}
    pprint(updated)
    final = {**updated, **cinema}
    pprint(final)
    return final

### TODO comparing dictionaries

AMONDO = amondo()
ILUZJON = iluzjon()
merge(AMONDO, ILUZJON)
