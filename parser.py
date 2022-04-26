import requests
from bs4 import BeautifulSoup

URL = 'https://auto.ria.com/uk/toplivo/ternopol/#refuel'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
HOST = 'https://index.minfin.com.ua/ua/markets/fuel/reg/ternopolskaya/'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r
    

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('table', class_='refuel table fuel-table-region azs h')

    return items

def delete_b_spaces(s):
    res = s
    while res[0] == ' ':
        res = res[1:]
    while res[-1] == ' ':
        res = res[:-1]
    return res
    

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        items = get_content(html.text)
        array_2d = get_2d_array_from_table(
            items[0], 
            mapper=lambda e: delete_b_spaces(e if 'область' not in e else 'Тернопільська область'),
            filter_1=lambda e: delete_b_spaces(e) != 'А-95+ А-95 А-92 ДП Газ'
        )
        beautiful_print(array_2d)

    else:
        print('Error')

def get_2d_array_from_table(table, mapper=lambda e: e, filter_1=lambda e: True, filter_2=lambda e: True):
    return [
        [
            mapper(col.getText())
        for col in (row.find_all('td') + row.find_all('th')) if filter_1(col.getText())]
    for row in table.find_all('tr') if filter_2(row)]

def simple_print(array_2d):
    print('\n'.join([
            ', '.join(row)
        for row in array_2d]))

def beautiful_print(array_2d):
    lens = [max(map(len, col)) for col in zip(*array_2d)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in array_2d]
    print('\n'.join(table))

parse()
input('Press ENTER to exit') 

