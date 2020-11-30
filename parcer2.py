import requests
import json
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import math
from length import length
from termcolor import colored
from itertools import groupby
URL = "https://cash.rbc.ru/cash/json/cash_rates/?city=1&currency=3&deal=buy&amount=100&_="

"""Получаем ссылку"""
BANKS = 0
spisok = ["Сбербанк", "АКБ ФОРА-БАНК", "Заубер Банк", "КБ Евроазиатский Инвестиционный Банк", "АКБ Трансстройбанк",
          "БАНК КРЕМЛЕВСКИЙ", "Банк БКФ", "КБ Евроазиатский Инвестиционный Банк", "КБ Спутник", "АКБ Ланта-Банк",
          "АКБ СЛАВИЯ", "АКБ Металлинвестбанк", "БАНК АГОРА", "БАНК МОСКВА-СИТИ", "Банк Таврический", "Банк ФИНАМ",
          "Банк ФК Открытие", "Газпромбанк ДО", "КБ Солидарность", "МТИ Банк", "НС Банк"]  # список банков
spisok_rate = []
distances=[]
banks_inf = []
banks=[]
spisok_buy=[]
spisok_sell=[]
# переменные для нахождения макс и мин продажи ,и нахождения ближ выгодной покупки или продажи
maxsell=0
minbuy=0
maxsellnear=0
minbuynear=0
def get_html(params):
    url = URL
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.77 YaBrowser/20.11.0.817 Yowser/2.5 Safari/537.36",
        "accept": "application/json, text/javascript, */*; q=0.01"
    }
    req = requests.get(url, headers)
    # print(req.text)
    params = params
    return get_content(req,params)


"""Создаем словарь с нужной нам информацией для болле просто использования """


def get_content(req,params):
    k = 0
    exist = 1
    content = json.loads(req.text)
    metro = []
    """Делаем собственный упрощенный словарь где уже будут нудные элементы"""
    for i in content["banks"]:
        """Проверка на существование ближайшего метро"""
        try:
            content["banks"][k]["metro"][0]
        except TypeError:
            exist = None
            metro.append("нет ближайшего метро")
        if exist is not None:
            for j in range(len(content["banks"][k]["metro"])):
                metro.append(content["banks"][k]["metro"][j][0])
        # print(metro)
        banks.append({  # создание словаря
            "bank": content["banks"][k]["name"],
            "buy": content["banks"][k]["rate"]["sell"],
            "sell": content["banks"][k]["rate"]["buy"],
            "metro": (", ".join(metro)),
            "latitude": content["banks"][k]["coordinates"][0],
            "longitude": content["banks"][k]["coordinates"][1],
        })
        # print(metro)
        metro.clear()
        exist = 1
        k += 1
    # print(banks)
    return banks_count(banks,params)



"""функция выводящая урощенный список банков для порльзователя"""


def banks_count(banks,params):
    """Сортировка банков"""
    for j in spisok:
        for i in range(len(banks)):
            if fuzz.partial_token_sort_ratio(j, banks[i]["bank"]) >= 90:  # Составление списка обменников с помощью совпадений
                spisok_rate.append("<i>%s</i>- <b>%s</b> / <b>%s</b>" % (j, banks[i]["sell"], banks[i]["buy"]))
                # print(j, '  ', banks[i]["bank"])
                break
    # print("\n".join(spisok_rate)) # Список доступных банков и их курсов
    text="\n".join(spisok_rate)
    if params=="text":
        # print(text)
        return text
    elif params=="distance":
        return banks
# print(get_html("text"))

"""нахождение ближайших банков по координатам"""


def get_distance(banks,params,latitude,longitude):
    names = []
    rates = []
    spisok_rate.clear()
    coordinates=[]
    spisok_text=[]
    for i in range(len(banks)):
        distances.append(length(latitude,longitude,banks[i]["latitude"], banks[i]["longitude"]))
    distances.sort(reverse=False)
    print(distances[:7])
    for i in range(0,7):
        try:  # Проверка на существование элемента
            distances[i]
        except IndexError:
            break
        else:
            for j in range(len(banks)):
                # print(length(latitude,longitude,banks[j]["latitude"],banks[i]["longitude"]))
                if distances[i] == length(latitude,longitude,banks[j]["latitude"],banks[j]["longitude"]):
                    names.append(banks[j]["bank"])
                    coordinates.append([banks[j]["latitude"],banks[j]["longitude"]])
                    rates.append([banks[j]["sell"],banks[j]["buy"]])
                    spisok_rate.append([banks[j]["bank"],banks[j]["sell"],banks[j]["buy"]])
                    spisok_text.append("<i>%s</i>- <b>%s</b> / <b>%s</b> (<i>%s</i>км)"%(banks[j]["bank"],banks[j]["sell"],banks[j]["buy"],length(latitude,longitude,banks[j]["latitude"],banks[j]["longitude"])))

    if params=="distance":
        text="\n".join(delete_copy(spisok_text))
        names=delete_copy(names)
        coordinates=delete_copy(coordinates)
        rates=delete_copy(rates)
        print(text)
        return text
    if params=="distance_buy":
        pass
    # print(names)
    # print(rates)


"""Функция по удалению дубликатов в массиве(удаляет даже вложенные списки)"""


def delete_copy(array):
    array1=[el for el, _ in groupby(array)]
    return array1

if __name__ == '__main__':
    get_html(params="text")


# for i in content["banks"]:
# print("Банк: ",content["banks"][k]["name"])
# print("Покупка: ",content["banks"][k]["rate"]["sell"])
# print("Продажа: ",content["banks"][k]["rate"]["buy"])
# try :
#     content["banks"][k]["metro"][0]
# except TypeError:
#     exist=None
#     print("Нет ближайшего метро\n")
# if exist is not None:
#     print("Метро: ", end="")
#     for j in range(len(content["banks"][k]["metro"])):
#         print(content["banks"][k]["metro"][j][0],end=", ")
#     print()
#     print()
# k+=1
# exist = 1
