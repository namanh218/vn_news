import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# connect to atlas mongodb
client = MongoClient(
    "mongodb+srv://m001-student:namanh123@sandbox-fwkp4.mongodb.net/test?retryWrites=true&w=majority")
db = client.news
collection = db.news_collection
# print all available db
print(client.list_database_names())

base_url = 'https://vnexpress.net/giao-duc-p1'

# Get the link


def parse_url(url):
    """
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features="html.parser")
        return soup

    except Exception as err:
        print(err)
        return ''


# def get_next_page(s):
#     return s.find_all('a', class_='btn-page next-page ')[0].get('href')

# Get all the content and titles
def get_content(url):
    s = parse_url(url)
    b = s.find_all('article', class_="item-news item-news-common off-thumb")
    res = s.find_all('a', class_="btn-page next-page ")[0].get('href')
    titles = [i.find_all('a')[0].string.replace('.', '')
              for i in b]
    des = [i.find_all('a')[1].string for i in b]
    a = list(map(lambda x: {x[0]: x[1]}, zip(titles, des)))

    del des
    del titles
    del s
    del b

    return a, res

# Save to db


def save_todb(d):
    return collection.insert_many(d)

# Get all pages


def get_all(url):
    while url:
        s, l = get_content(url)
        url = 'http://vnexpress.net'+l
        if len(s) == 0:
            continue
        print(url)
        save_todb(s)
        if len(l) == 0:
            print('end')
            break
        print('next')
    return


get_all(base_url)
