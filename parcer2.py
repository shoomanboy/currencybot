import requests
import json
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import math
from length import length

URL = "https://cash.rbc.ru/cash/json/cash_rates/?city=1&currency=3&deal=buy&amount=100&_="

"""Получаем ссылку"""
latitude = 55.845415
longitude = 37.340476
BANKS = 0
spisok = ["Сбербанк", "АКБ ФОРА-БАНК", "Заубер Банк", "КБ Евроазиатский Инвестиционный Банк", "АКБ Трансстройбанк",
          "БАНК КРЕМЛЕВСКИЙ", "Банк БКФ", "КБ Евроазиатский Инвестиционный Банк", "КБ Спутник", "АКБ Ланта-Банк",
          "АКБ СЛАВИЯ", "АКБ Металлинвестбанк", "БАНК АГОРА", "БАНК МОСКВА-СИТИ", "Банк Таврический", "Банк ФИНАМ",
          "Банк ФК Открытие", "Газпромбанк ДО", "КБ Солидарность", "МТИ Банк", "НС Банк"]  # список банков
spisok_rate = []
distances=[]
names=[]
rates=[]

def get_html():
    url = URL
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.77 YaBrowser/20.11.0.817 Yowser/2.5 Safari/537.36",
        "accept": "application/json, text/javascript, */*; q=0.01"
    }
    req = requests.get(url, headers)
    # print(req.text)
    return get_content(req)


"""Создаем словарь с нужной нам информацией для болле просто использования """


def get_content(req):
    k = 0
    exist = 1
    content = json.loads(req.text)
    banks = []
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
    # print(k)
    return banks_count(banks)


"""функция выводящая урощенный список банков для порльзователя"""


def banks_count(banks):

    """Сортировка банков"""
    for j in spisok:
        for i in range(len(banks)):
            if fuzz.partial_token_sort_ratio(j, banks[i]["bank"]) >= 90:
                spisok_rate.append("%s- %s / %s" % (j, banks[i]["sell"], banks[i]["buy"]))
                # print(j, '  ', banks[i]["bank"])
                break
    print("\n".join(spisok_rate))
    return get_distance(banks)


def get_distance(banks):
    for i in range(len(banks)):
        distances.append(length(latitude, longitude, banks[i]["latitude"], banks[i]["longitude"]))
    distances.sort(reverse=False)
    print(distances[:5])
    for i in range(0,5):
        for j in range(len(banks)):
            # print(length(latitude,longitude,banks[j]["latitude"],banks[i]["longitude"]))
            if distances[i] == length(latitude,longitude,banks[j]["latitude"],banks[j]["longitude"]):
                names.append(banks[j]["bank"])
                rates.append([banks[j]["sell"],banks[j]["buy"]])
    print(names)
    print(rates)

if __name__ == "__main__":
    get_html()

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
