import requests
from bs4 import BeautifulSoup

URL = "https://cbr.ru/currency_base/"
"""Заголовки для того чтобы не заблочило)))"""
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.126 Yowser/2.5 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
HOST="https://cbr.ru"


def get_html(url, params=None):  # Функция где будут задаваться параметры(обращение к определенной странице, заголовку)
    r = requests.get(url, headers=HEADERS, params=params)
    return r



def get_content(html):
    soup=BeautifulSoup(html, "html.parser")
    items=soup.find_all("div", class_="document-regular")
    headline=[]
    for item in items:
        headline.append({
            "title":item.find("span",class_="document-regular_name_visible").get_text(),
            "link":HOST+item.find("div", class_="document-regular_name").find('a').get('href')

        })
    print(headline)



def parse():
    html=get_html(URL)
    if html.status_code==200:
        get_content(html.text)
    else:
        print("Error!")

parse()