from telegram import bot, ReplyKeyboardRemove, ReplyKeyboardMarkup, PhotoSize
from telegram.ext import Updater, CallbackContext, Filters, MessageHandler, ConversationHandler, CommandHandler, \
    CallbackQueryHandler
from settings_bot_currency import TG_Token
from settings_bot_currency import id_name, mdb
import os
from PIL import Image
import parcer2
from parcer2 import URL, get_html, get_content, banks_count
import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
import pymongo

MONGODB_LINK = "mongodb+srv://shoomaher:7598621zhora@telegrambot.fls8z.mongodb.net/telegrambot?retryWrites=true&w=majority"
MONGODB = "telegramcurrency"

button_currency = "Валюты"
button_help = "/help"
button_end = "/end"
button_menu = "/menu"
spisok_currency = []
letter_code = []
units = []
rate = []
value = 0
button_location = "Отправить геопозицию"

ind = -1  # Переменная для сохранения номера элемента в БД по валютам


def dontknow(bot, update):  # Если непривально введена команда,то будет отправляться пользователю данная команда
    bot.message.reply_text(text='Я вас не понимаю,нажмите на команду')


def message_handler(bot, update):  # Обработчик сообщений после ввода команды запуска
    my_keyboard = ReplyKeyboardMarkup([[button_currency], [button_help], [button_end,button_location]])
    name = bot.message.chat.first_name
    bot.message.reply_text(
        text="Привет %s, не хочешь узнать курсы валют и их динамику?\nЕсли да,то переходи по кнопке нижу!" % name,
        reply_markup=my_keyboard)
    return "spisok comand"


def spisok_comand(bot,update):  # данная функция перенаправляет пользователя на нужное направление в зависимости его запроса
    my_keyboard = ReplyKeyboardMarkup([[button_currency], [button_help, button_end]])
    if bot.message.text == button_help:
        bot.message.reply_text(
            text="Данный бот способен показывать курсы валют по вашему выбору и также может анализировать ее динамику\nКоманда: 'Валюты' перенаправит вас в меню по валютам\nКоманда: '/end' завершит диалог с ботом  ")
        return "spisok comand"
    if bot.message.text == button_end:
        bot.message.reply_text(
            text="До скорой встречи!\nЕсли захочешь узнать свежую информацию, то напиши команду '/start'!",
            reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    if bot.message.text == button_currency:
        currency_keyboard = ReplyKeyboardMarkup(
            [["Определенная валюта сегодня"], ["Курс валюты в выбранные даты"], [button_menu]])
        bot.message.reply_text(text="Вы находитесь в меню динамики валюты\nНажмите на нужную вам команду",
                               reply_markup=currency_keyboard)
        return "currency menu"
    if bot.message.text == button_menu:
        bot.message.reply_text(text="Вы находитесь в главном меню!", reply_markup=my_keyboard)
        return "spisok comand"
    if bot.message.text == button_location:
        bot.message.reply_text(text="Чтобы отправить нам геопозицию нажмите на скрепку,затем прикрепить геопозицию",reply_markup=ReplyKeyboardRemove())
        return "get location"


def currency_spisok_command(bot, update):  # Перенаправляет по направления блока (валюта)
    """Удаление граифка"""
    chat_id = bot.message.chat_id
    myfile = "graph_%s.png" % chat_id
    ## If file exists, delete it ##
    if os.path.isfile(myfile):
        os.remove(myfile)
    else:  ## Show an error ##
        print("Error: %s file not found" % myfile)
    global value
    spisok_currency.clear()
    letter_code.clear()
    units.clear()
    rate.clear()
    if bot.message.text == "Определенная валюта сегодня":
        receive = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        data = json.loads(receive.text)
        for valute in data["Valute"]:
            spisok_currency.append([data["Valute"]["%s" % valute]["Name"]])
        my_keyboard = ReplyKeyboardMarkup(spisok_currency)
        bot.message.reply_text(text="Выберете валюту чтобы увидеть информацию по ней за сегодня",
                               reply_markup=my_keyboard)
        return "currency statistics"
    if bot.message.text == "Курс валюты в выбранные даты":
        result = mdb.find_one({"_id": id_name})
        for i in range(len(result["currency"])):  # создание клавиатуры из списка доступных валют
            letter_code.append([result["letter code"][i]])
            spisok_currency.append([result["currency"][i]])
        my_keyboard = ReplyKeyboardMarkup(spisok_currency)
        bot.message.reply_text(text="Выберете валюту чтобы увидеть информацию по ней за промежуток времени!",
                               reply_markup=my_keyboard)
        return "date input"
    if bot.message.text == button_menu:
        my_keyboard = ReplyKeyboardMarkup([[button_currency], [button_help, button_end]])
        bot.message.reply_text(text="Вы находитесь в главном меню", reply_markup=my_keyboard)
        return "spisok comand"


def currency_statistics(bot, update):
    global ind, value
    value = bot.message.text
    receive = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    data = json.loads(receive.text)
    for valute in data["Valute"]:
        if value == data["Valute"]["%s" % valute]["Name"]:
            ind = valute
            continue
    bot.message.reply_text(text="Валюта: %s\nСокращенное название: %s\nКоличество: %s\nКурс: %s рублей" % (
        data["Valute"]["%s" % ind]["Name"], data["Valute"]["%s" % ind]["CharCode"],
        data["Valute"]["%s" % ind]["Nominal"],
        data["Valute"]["%s" % ind]["Value"]))
    my_keyboard = ReplyKeyboardMarkup([[button_currency], [button_help, button_end]])
    bot.message.reply_text(text="Вы находитесь в главном меню", reply_markup=my_keyboard)
    return "spisok comand"


def date_input(bot, update):
    global value
    value = bot.message.text
    bot.message.reply_text(
        text="Введите диапозон дат как на примере:<2020-10-25 2020-11-5>\n<Год-месяц-число Год-месяц-число>\nБез треугольных скобок!!!",
        reply_markup=ReplyKeyboardRemove())
    return "currency certain statistics"


def currency_certain_statistics(bot, update):
    chat_id = bot.message.chat_id  # сохранение id
    spisok = []
    date = []
    global ind, value
    for i in range(len(spisok_currency)):  # Нахождение соответсвуюшего элемента в БД
        if spisok_currency[i] == [value]:
            ind = i
            continue
    code = str(letter_code[ind]).replace("['", "")  # Удаление лишних символов
    code = code.replace("']", "")  # Удаление лишних символов
    currency_start_date, currency_end_date = map(str, bot.message.text.split(" "))
    currency_start_date = pd.to_datetime(currency_start_date)  # Преобразование в дату
    currency_end_date = pd.to_datetime(currency_end_date)  # Преобразование в дату
    daterange = pd.date_range(currency_start_date, currency_end_date)  # Создание диапазона по датам
    for single_date in daterange:
        receive = requests.get("https://www.cbr-xml-daily.ru/archive/%s/daily_json.js" % (
            single_date.strftime("%Y/%m/%d")))  # Отправляем запрос к странице,где сначала год,месяц,число
        data = json.loads(receive.text)  # Преобразование в Json файл
        try:  # Условие при котором проверяется элемент на существование в словаре
            data["error"]
        except KeyError:  # Если при проверке этого элемента возникает ошибка на его существование, то выводится курс валюты
            spisok.append(data["Valute"]["%s" % code]["Value"])  # Сохранение курса валюты в определенную дату
            date.append(single_date.strftime("%Y-%m-%d"))  # Сохранение даты
    print(date)
    print(spisok)
    """Построение графика в питоне """
    df = pd.DataFrame({"date": date, "value": spisok})  # Построение графика в pandas с помощью dataframe
    df["date"] = pd.to_datetime(df["date"])  # Присвоение датам значение даты
    plt.plot(df["date"], df["value"], lw=1, ls='-', marker='o', markersize=7)  # создание осей
    plt.title("График изменения валюты: %s" % value)
    plt.ylabel("Курс валюты")
    plt.grid(True)
    plt.gcf().autofmt_xdate()  # Форматирование графика чтобы не наезжал шрифт
    plt.savefig("graph_%s" % chat_id)  # сохранение графика
    graph = open("graph_%s.png" % chat_id, "rb")  # открытие графика в переменной
    update.bot.send_photo(chat_id=bot.message.chat_id, photo=graph)  # Отправка графика пользователю на id пользователя
    plt.clf()
    """Вывод данных за промежуток времени"""
    # for i,item in enumerate(date):
    #     date[i]+=" курс: %s рубля"%spisok[i]
    # bot.message.reply_text(text="\n".join(date))
    my_keyboard = ReplyKeyboardMarkup([[button_currency], [button_menu, button_end]])
    bot.message.reply_text(text="Выбери команду", reply_markup=my_keyboard)

    return "spisok comand"


"""Получаем геопозицию пользователя"""


def get_location(bot, update):
    print(bot.message.location)
    location=bot.message.location
    latitude=location["latitude"]
    longitude=location["longitude"]
    print(latitude,longitude)
    bot.message.reply_text(text="Сейчас подберем ближайший к вам обменник {}".format(bot.message.chat.first_name))
    return"spisok comand"


"""Обмен валюты"""



def main():  # Основные параметры работы бота(Токен,диалог)
    print("Бот с курсами валют запущен")
    updater = Updater(token=TG_Token, use_context=True)
    start_handler = updater.dispatcher.add_handler(
        ConversationHandler(entry_points=[CommandHandler("start", message_handler)],
                            states={
                                "spisok comand": [MessageHandler(Filters.regex("/help|/end|Валюты|/menu|Отправить геопозицию"),spisok_comand)],
                                "currency menu": [MessageHandler(Filters.regex("Определенная валюта сегодня|Курс валюты в выбранные даты|/menu"),currency_spisok_command)],
                                "currency statistics": [MessageHandler(Filters.text, currency_statistics)],
                                "date input": [MessageHandler(Filters.text, date_input)],
                                "currency certain statistics": [MessageHandler(Filters.text, currency_certain_statistics)],
                                "get location": [MessageHandler(Filters.location, get_location)]
                            },
                            fallbacks=[MessageHandler(Filters.text | Filters.video | Filters.document | Filters.photo,
                                                      dontknow)]
                            )

    )
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
