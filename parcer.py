from bs4 import BeautifulSoup
import requests
import pymongo
from settings_bot_currency import mdb, id_name
from array import *

# a = []
# b = []
# spisok_currency = []
# letter_code = []
# units = []
# rate = []
"""Подключение к парсеру Ежедневной валюты"""
# receive = requests.get("https://cbr.ru/currency_base/daily/")  # Отправляем запрос к странице
# page = BeautifulSoup(receive.text, "html.parser")  # подключаем html-парсер, получаем текст страницы
# find = page.select(".data")  # из из страницы html получаем class="data"
# print(find)

""" Работа с инфомрацией, полученной из парсера"""
# for text in find:  # работаем с информацией полученной из class="data"
#     page = (text.getText())  # Получаем тексти присваеваем его массиву page
#     a = page.split("\n")  # убираем из массива переход на следующую строку
# a = [x for x in a if x]  # удаляем пустые элементы массива('')
# print((len(a) - 5) // 5)

"""удаляем первые 5 элементов массива тк они бесполезны"""
# for i in range(5):  # удаляем первые 5 элементов массива тк они бесполезны
#     a.pop(0)
# print(a)

# for i in range(0, len(a), 5):  # создание массива из списков
#     b.append([a[i], a[i + 1], a[i + 2], a[i + 3], a[i + 4]])
# print(b)

"""Обнуление БД"""
# result = mdb.update_one({"_id": id_name}, {"$set": {"number code": [], "letter code": [], "units": [], "currency": [],
#                                                     "rate": []}})  # обнуление данных с курсом

"""Заполнение БД данными о валюте"""
# for i in range(len(b)):
#     result = mdb.find_one_and_update({"_id": id_name}, {
#         "$push": {"number code": b[i][0], "letter code": b[i][1], "units": b[i][2], "currency": b[i][3],
#                   "rate": b[i][4]}})

"""Создание массивов!"""
# for i in range(len(b)):
#     currency.append([b[i][3]])
# print(currency)

# result = mdb.find_one({"_id": id_name})
# print(len(result["currency"]))
# print(result["currency"])

# """Создание массива с названием валют"""
# for i in range(len(result["currency"])): # заполнение массива из БД с названиями валют
#     spisok_currency.append([result["currency"][i]])
# print(len(result["currency"]))
#
# """Создание массива с кодами валют"""
# for i in range(len(result["letter code"])): # заполнение массива из БД с сокращенными названиями валют
#     letter_code.append([result["letter code"][i]])
# print(len(result["letter code"]))
#
# """Создание массива с юнитами валют"""
# for i in range(len(result["units"])): # заполнение массива из БД с юнитами валюты
#     units.append([result["units"][i]])
# print(len(result["units"]))
#
# """Создание массива курсом валют"""
# for i in range(len(result["rate"])): # заполнение массива из БД с курсом валюты
#     rate.append([result["rate"][i]])
# print(len(result["rate"]))
#
#


"""Парсер с ФБК по Москве """
#   будет парсинг ближайших банкоматов
#   парсинг курса покупки и продажи
URL = "https://cash.rbc.ru/?currency=3&city=1&deal=buy&amount=100"  # покупка валюты
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.77 YaBrowser/20.11.0.817 Yowser/2.5 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}


""" Работа с парсером и работа с текстом """


def spisok_banks():
    def get_html(url, params=None):
        r = requests.get(url, headers=HEADERS, params=params)
        return r
    """Извлечение текста из ссылки"""
    def get_content(html):
        soup = BeautifulSoup(html, "html.parser")
        items = soup.find("div", class_="quote__office__content js-office-content")  # Выбираем блок с информации о доступных банках
        items = items.getText().split("\n")  # Убириаем пробелы
        banks = [x for x in items if x]  # Убираем пустые элементы массива
        # banks=list(filter(None,items)  # Убираем пустые элементы массива
        """Циклы по удалению проеблов до и после слова"""
        for i in range(len(banks)):
            banks[i] = banks[i].strip()
        banks = [x for x in banks if x]
        print(len(banks)//12)
        return sort_banks(banks)


    """Создание массивов с инфомрацией по банкоматам"""
    def sort_banks(banks):
        filtered_banks=[]
        for i in range(0,len(banks),12):  # Название,номер, покупка, продажа,метро
            filtered_banks.append([banks[i],banks[i+1],banks[i+2],banks[i+4],banks[i+9]])
        banks.clear()
        banks=filtered_banks
        print(banks)



    """Обращение к ссылке и проверка на ее работоспособность"""
    def parse():
        html = get_html(URL)
        if html.status_code == 200:
            get_content(html.text)
        else:
            print("error")

    parse()


spisok_banks()

