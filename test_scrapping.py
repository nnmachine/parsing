import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_creation import Users, Base


URL = 'https://webscraper.io/test-sites/tables'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
           'accept': '*/*'
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('table', class_='table table-bordered')
    users = []
    for item in items:
        users.append(item.find_all('td'))
    real_users = []
    i = 1
    index = 0
    for user in users:
        for u in user:
            if i % 4 == 1:
                real_users.append({'id': str(u)[4:len(str(u))-5],
                                   'first_name': '',
                                   'last_name': '',
                                   'nickname': ''})
            if i % 4 == 2:
                real_users[index]['first_name'] = str(u)[4:len(str(u))-5]
            if i % 4 == 3:
                real_users[index]['last_name'] = str(u)[4:len(str(u))-5]
            if i % 4 == 0:
                real_users[index]['nickname'] = str(u)[4:len(str(u))-5]
                index += 1
            i += 1
    users = []
    for user in real_users:
        if user not in users and user['id'] != '-':
            users.append(user)
    return users


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        print(html)
        return get_content(html)
    else:
        print('error')


def db_add(list):
    engine = create_engine('sqlite:///sqllitexample.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    for user in list:
        id = user['id']
        first_name = user['first_name']
        last_name = user['last_name']
        nickname = user['nickname']
        new_user = Users(id=id, first_name=first_name, last_name=last_name, nickname=nickname)
        session.add(new_user)
        session.commit()


print(parse())
db_add(parse())
