import requests
import pandas as pd
import json

# currency_start_date = input()  # В водим дату начала либо через дефис либо через слеш либо через пробел
# currency_end_date = input()  # Вводим дату конца либо через дефис либо через слеш либо через пробел
# currency_start_date = pd.to_datetime(currency_start_date)  # Преобразование в дату
# currency_end_date = pd.to_datetime(currency_end_date)  # Преобразование в дату

# currency_start_date,currency_end_date=map(str,input().split(" "))
# currency_start_date = pd.to_datetime(currency_start_date)  # Преобразование в дату
# currency_end_date = pd.to_datetime(currency_end_date)  # Преобразование в дату

""" Цикл по выводу информации по курсу валют в определенные даты"""

# daterange = pd.date_range(currency_start_date, currency_end_date)  # Создание диапазона по датам
# for single_date in daterange:
#     receive = requests.get("https://www.cbr-xml-daily.ru/archive/%s/daily_json.js" % (single_date.strftime("%Y/%m/%d")))  # Отправляем запрос к странице,где сначала год,месяц,число
#     data = json.loads(receive.text)  # Преобразование в Json файл
#     try:  # Условие при котором проверяется элемент на существование в словаре
#         data["error"]
#     except KeyError:  # Если при проверке этого элемента возникает ошибка на его существование, то выводится курс валюты
#         # data["error"]=None
#         print(data["Valute"]["EUR"]["Value"])  # Вывод курса валюты
"""Цикл по получению информации за сегодняшний день"""
receive=requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
data = json.loads(receive.text)
print(data["Valute"])

for valute in data["Valute"]:

    print(valute,"=",data["Valute"]["%s"%valute]["Name"])


