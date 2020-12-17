import requests
import json
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from length import length,length_top5
from itertools import groupby
import googlemaps
from operator import itemgetter
URL = "https://cash.rbc.ru/cash/json/cash_rates/?city=1&currency=3&deal=buy&amount=100&_="  # Доллар
# # URL = "https://cash.rbc.ru/cash/json/cash_rates/?city=1&currency=2&deal=buy&amount=100&_="  # Евро
"""Получаем ссылку"""
BANKS = 0
spisok = ["Сбербанк", "АКБ ФОРА-БАНК", "Заубер Банк", "КБ Евроазиатский Инвестиционный Банк", "АКБ Трансстройбанк",
          "БАНК КРЕМЛЕВСКИЙ", "Банк БКФ", "КБ Спутник", "АКБ Ланта-Банк", "АКБ СЛАВИЯ", "АКБ Металлинвестбанк",
          "БАНК АГОРА", "БАНК МОСКВА-СИТИ", "Банк Таврический", "Банк ФИНАМ", "Банк ФК Открытие",
          "Газпромбанк ДО", "КБ Солидарность", "МТИ Банк", "НС Банк"]  # список банков
phones=["88005555550","88001009889","88007754454","88005555603","88005053773",
        "84992418814","84955140810","84951421720","84959570000","84959692415","88002509797",
        "84957887248","84959818503","88007755712","88002004400","88004444400",
        "84959137474","88007009220","84957398800","88005554324"]  # список номеров банков соответсвенно
links=["https://www.sberbank.ru/ru/person/additional/operations","https://www.forabank.ru/offices/filter/c-moskva/t-otdeleniya_i_kassy/","https://www.sauberbank.com/msk/services/currencyrates/","https://eab.ru/","https://www.transstroybank.ru/chastnym-klientam/konvertor-valyut/",
       "https://kremlinbank.ru/","https://www.cfb.ru/about/currency/","http://www.banksputnik.ru/kursy-valyut/","https://www.lanta.ru/private/?moscow","http://www.slaviabank.ru/","https://metallinvestbank.ru/private/foreign-exchange-transactions/",
       "http://kbagora.ru/","http://www.mcbank.ru/","https://www.tavrich.ru/cur/","https://finambank.ru/person/currency","https://www.open.ru/exchange-person",
       "https://www.gazprombank.ru/personal/courses/","https://solid.ru/retail/kursy-valyut/mos/","https://www.mti-bank.ru/","https://nsbank-exchange.ru/"]
banks_inf = []

# переменные для нахождения макс и мин продажи ,и нахождения ближ выгодной покупки или продажи


def get_html(url,params):
    url = url
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
    banks = []
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
    word=0
    """Сортировка банков"""
    spisok_rate=[]
    for j in range(len(spisok)):
        for i in range(len(banks)):
            if fuzz.partial_token_sort_ratio(spisok[j], banks[i]["bank"]) >= 90:  # Составление списка обменников с помощью совпадений
                word="<b>%s</b> / <b>%s</b> <a href='%s'>%s</a>\nТелефон: %s" % ( banks[i]["sell"], banks[i]["buy"],links[j],spisok[j],phones[j])
                if word not in spisok_rate:
                    spisok_rate.append("<b>%s</b> / <b>%s</b> <a href='%s'>%s</a>\nТелефон: %s" % ( banks[i]["sell"], banks[i]["buy"],links[j],spisok[j],phones[j]))
                    break
    # print("\n".join(spisok_rate)) # Список доступных банков и их курсов
    text="\n".join(delete_copy(spisok_rate))
    if params=="text":
        # print(text)
        return text
    elif params=="distance":
        return banks
# print(get_html("text"))

"""нахождение ближайших банков по координатам"""


def get_distance(banks,params,latitude,longitude):
    distances = []
    names = []
    rates = []
    spisok_rate=[]
    spisok_rate.clear()
    coordinates=[]
    coordinates.clear()
    spisok_text=[]
    spisok_text.clear()
    spisok_data=[]
    spisok_data.clear()
    spisok_buy = []
    spisok_buy.clear()
    spisok_buy_sorted=[]
    spisok_buy_sorted.clear()
    spisok_sell = []
    spisok_sell.clear()
    spisok_sell_sorted=[]
    spisok_sell_sorted.clear()
    maxsell = 0
    lenmax=[]
    imax=-1
    minbuy = 999999999
    imin=-1
    lenmin=[]
    maxsellnear = 0
    minbuynear = 0
    clon=0
    """Поиск максимального и минимального курса продажи покупки"""
    for i in range(len(banks)):
        if float(banks[i]["sell"])>float(maxsell):
            maxsell=banks[i]["sell"]
        if float(banks[i]["buy"])<float(minbuy):
            minbuy=banks[i]["buy"]

    """Сохранение всех максимальных и минимальных элементов"""
    for i in range(len(banks)):
        if banks[i]["sell"]==maxsell:
            spisok_buy.append([banks[i]["latitude"], banks[i]["longitude"], length(latitude,longitude,banks[i]["latitude"], banks[i]["longitude"]), i,banks[i]["sell"],banks[i]["buy"],banks[i]["bank"]])
        if banks[i]["buy"]==minbuy:
            spisok_sell.append([banks[i]["latitude"], banks[i]["longitude"], length(latitude,longitude, banks[i]["latitude"], banks[i]["longitude"]), i,banks[i]["sell"],banks[i]["buy"],banks[i]["bank"]])
    spisok_buy.sort(key=itemgetter(2))
    spisok_sell.sort(key=itemgetter(2))
    for i in range(0,2):
        try:
            spisok_buy[i]
        except IndexError:
            break
        else:
            j=spisok_buy[i][3]
            lenmax.append(length_top5(latitude,longitude,banks[j]["latitude"],banks[j]["longitude"]))
    imax=min(lenmax)
    spisok_buy[0][2]=imax
    for i in range(0,2):
        try:
            spisok_sell[i]
        except IndexError:
            break
        else:
            j=spisok_sell[i][3]
            lenmin.append(length_top5(latitude,longitude,banks[j]["latitude"],banks[j]["longitude"]))
    imin=min(lenmin)
    spisok_sell[0][2]=imin
    try:
        spisok_buy_sorted[i]
    except IndexError:
        spisok_buy_sorted.append(spisok_buy[0])
    maxsell=spisok_buy_sorted[0]
    try:
        spisok_sell_sorted[i]
    except IndexError:
        spisok_sell_sorted.append(spisok_sell[0])
    minbuy=spisok_sell_sorted[0]
    # "<i>%s</i>- <b>%s</b> / <b>%s</b> (<i>%s</i>км)" % (spisok_data[i][0], spisok_data[i][1], spisok_data[i][2], spisok_data[i][3]

    # maxsell = "🏦<b>%s</b> / <b>%s</b> <a href='%s'>%s</a> (<i>%s</i>км)"
    # покупка / продажа банк расстояние
    maxsell="🏦<b>%s</b> / <b>%s</b> <a href='%s'>%s</a> (<i>%s</i>км)" % (maxsell[4],maxsell[5],link(latitude,longitude,maxsell[0],maxsell[1]),maxsell[6],maxsell[2])
    minbuy="🏦<b>%s</b> / <b>%s</b> <a href='%s'>%s</a> (<i>%s</i>км)" % (minbuy[4],minbuy[5],link(latitude,longitude,minbuy[0],minbuy[1]),minbuy[6],minbuy[2])
    # print(maxsell)
    # print(minbuy)
    """Подсчет расстояния с помощью расстояния между точками, затем подсчет расстояния в топ5 через googlemapsapi"""
    distances.clear()
    for i in range(len(banks)):
        distances.append(length(latitude,longitude,banks[i]["latitude"], banks[i]["longitude"]))
    distances.sort(reverse=False)
    # print(distances[:7])
    for i in range(0,7):
        try:  # Проверка на существование элемента
            distances[i]
        except IndexError:
            break
        else:
            """создание новых массивов потому что я бомж и не могу соритировать относительно расстояния из гугла"""
            """в этих массивах сохранены значения первых семи обменников по близости"""
            for j in range(len(banks)):
                # print(length(latitude,longitude,banks[j]["latitude"],banks[i]["longitude"]))
                if distances[i] == length(latitude,longitude,banks[j]["latitude"],banks[j]["longitude"]):
                    names.append(banks[j]["bank"])
                    coordinates.append([banks[j]["latitude"],banks[j]["longitude"]])
                    rates.append([banks[j]["sell"],banks[j]["buy"]])
                    spisok_rate.append([banks[j]["bank"],banks[j]["sell"],banks[j]["buy"]])
    """Создание списка уже из топ5 обменников но с Googlemaps"""
    """Удаление дубликатов чтобы получить списки с сохраненными данными без повторов"""
    names = delete_copy(names)
    # print(names)
    coordinates = delete_copy(coordinates)
    # print(coordinates)
    spisok_rate=delete_copy(spisok_rate)
    # print(spisok_rate)
    for i in range(0, 5):
        try:  # Проверка на существование элемента
            names[i]
        except IndexError:
            break
        else:  # список в котором сохранены все данные,для того чтобы делать сортировку относительно любогу параметра
            # затем можно отсортированный список использовать для создания списка из строчек с отсортированными данными
            spisok_data.append([names[i], spisok_rate[i][1],spisok_rate[i][2], length_top5(latitude, longitude, coordinates[i][0], coordinates[i][1]),latitude, longitude, coordinates[i][0], coordinates[i][1]])
    """Ближайшие банки"""
    if params=="distance":
        spisok_data.sort(key=itemgetter(3))
        for i in range(len(spisok_data)):
            spisok_text.append("🏦<b>%s</b> / <b>%s</b> <a href='%s'>%s</a> (<i>%s</i>км)" % (spisok_data[i][1],spisok_data[i][2],link(spisok_data[i][4],spisok_data[i][5],spisok_data[i][6],spisok_data[i][7]),spisok_data[i][0], spisok_data[i][3]))
        text="\n".join(spisok_text)
        # print(text)
        return text
    """Выгодная покупка(банк покупает по самому высоку курсу)"""
    if params=="distance_buy":
        spisok_data.sort(key=itemgetter(1))
        for i in range(len(spisok_data)):
            spisok_text.append("🏦<b>%s</b> / <b>%s</b> <a href='%s'>%s</a> (<i>%s</i>км)" % (spisok_data[i][1],spisok_data[i][2],link(spisok_data[i][4],spisok_data[i][5],spisok_data[i][6],spisok_data[i][7]),spisok_data[i][0], spisok_data[i][3]))
        # print("\n".join(spisok_text))
        if maxsell not in spisok_text:
            spisok_text.insert(0,maxsell)
        text = "\n".join(spisok_text)
        return text
    """Выгодная продажа(банк продает по самому низкому курсу)"""
    if params=="distance_sell":
        spisok_data.sort(key=itemgetter(2))
        for i in range(len(spisok_data)):
            spisok_text.append("🏦<b>%s</b> / <b>%s</b> <a href='%s'>%s</a> (<i>%s</i>км)" % (spisok_data[i][1],spisok_data[i][2],link(spisok_data[i][4],spisok_data[i][5],spisok_data[i][6],spisok_data[i][7]),spisok_data[i][0], spisok_data[i][3]))
        if minbuy not in spisok_text:
            spisok_text.insert(0,minbuy)
        text = "\n".join(spisok_text)
        return text
    # print(names)
    # print(rates)


def link(latitude, longitude,latitude1,longitude1):
    link='https://yandex.ru/maps/213/moscow/?ll=%2C&mode=routes&rtext={0}%2C{1}~{2}%2C{3}&rtt=auto&ruri=ymapsbm1%3A%2F'.format(latitude, longitude,latitude1,longitude1)
    # print(link)
    return link


"""Функция по удалению дубликатов в массиве(удаляет даже вложенные списки)"""


def delete_copy(array):
    array1=[el for el, _ in groupby(array)]
    return array1

