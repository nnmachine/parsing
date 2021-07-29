import requests
from bs4 import BeautifulSoup
import csv
import io


URL = 'https://www.kinopoisk.ru/lists/navigator/?quick_filters=available_online&tab=online'
HOST = 'https://www.kinopoisk.ru'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
           'accept': '*/*'}
FILE = 'movies.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def save_file(items, path):
    with io.open(path, 'w', newline='', encoding='utf8') as file:
        writer = csv.writer(file)
        writer.writerow(['Название', 'Название на ориге', 'Рейтинг', 'Ссылка', 'Дополнительно'])
        for item in items:
            writer.writerow([item['title'],
                             item['title_original'],
                             item['rating'],
                             item['link'],
                             item['additional']])


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='paginator__page-number')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='desktop-seo-selection-film-item selection-list__film')
    films = []
    for item in items:
        films.append({
            'title': item.find('p', class_='selection-film-item-meta__name').get_text(),
            'title_original': item.find('p', class_='selection-film-item-meta__original-name').get_text(),
            'rating': item.find('span', class_='selection-film-item-poster__rating selection-film-item-poster__rating_positive'),
            'link': HOST+item.find('a', class_='selection-film-item-meta__link').get('href'),
            'additional': item.find('p', class_='selection-film-item-meta__meta-additional'),
        })
    print(items)
    return films


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        movies = []
        pages_count=get_pages_count(html.text)
        #for page in range(1, pages_count+1):
        #    print(f'парсинг {page} из {pages_count}')
        #    html = get_html(URL, params={'page': page})
        #    movies.extend(get_content(html.text))
        #save_file(movies, FILE)
        print(len(movies))
        films = get_content(html.text)
    else:
        print('Error')


parse()
