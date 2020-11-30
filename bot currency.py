from telegram import bot, ReplyKeyboardRemove, ReplyKeyboardMarkup, PhotoSize, ParseMode, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram.ext import Updater, CallbackContext, Filters, MessageHandler, ConversationHandler, CommandHandler, \
    CallbackQueryHandler
from settings_bot_currency import TG_Token
from settings_bot_currency import id_name, mdb
import os
from PIL import Image
import parcer2
from parcer2 import URL, get_html, get_content, banks_count, get_distance
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
letter_code = []  # сокращенное название валюты
units = []  # колличество купюр
rate = []  # курс валюты
value = 0  # поиск выбранной валюты для ее статистике --->в функцие)
button_location = "Отправить геопозицию"
button_exchange = "Обмен валюты"

ind = -1  # Переменная для сохранения номера элемента в БД по валютам


def dontknow(bot, update):  # Если непривально введена команда,то будет отправляться пользователю данная команда
    bot.message.reply_text(text='Я вас не понимаю,нажмите на команду')


"""Старт"""


def message_handler(bot, update):  # Обработчик сообщений после ввода команды запуска
    my_keyboard = ReplyKeyboardMarkup([[button_exchange], [button_currency], [button_end]])
    name = bot.message.chat.first_name
    bot.message.reply_text(
        text="Привет %s, не хочешь узнать курсы валют и их динамику?\nЕсли да,то переходи по кнопке нижу!" % name,
        reply_markup=my_keyboard)
    return "spisok comand"


"""Основной список команд"""


def spisok_comand(bot,
                  update):  # данная функция перенаправляет пользователя на нужное направление в зависимости его запроса
    my_keyboard = ReplyKeyboardMarkup([[button_exchange], [button_currency], [button_end]])
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
        receive = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        data = json.loads(receive.text)
        text = "<b>%s</b>-<i>%s</i>\n<b>%s</b>-<i>%s</i>" % (
        data["Valute"]["USD"]["Name"], data["Valute"]["USD"]["Value"], data["Valute"]["EUR"]["Name"],
        data["Valute"]["EUR"]["Value"])
        currency_keyboard = ReplyKeyboardMarkup(
            [["Определенная валюта сегодня"], ["Курс валюты в выбранные даты"], [button_menu]])
        bot.message.reply_text(text=text, parse_mode=ParseMode.HTML)
        bot.message.reply_text(text="Вы находитесь в меню динамики валюты\nНажмите на нужную вам команду",
                               reply_markup=currency_keyboard)
        return "currency menu"
    if bot.message.text == button_menu:
        bot.message.reply_text(text="Вы находитесь в главном меню!", reply_markup=my_keyboard)
        return "spisok comand"
    # if bot.message.text == button_location:
    #     bot.message.reply_text(text="Чтобы отправить нам геопозицию нажмите на скрепку,затем прикрепить геопозицию",
    #                            reply_markup=ReplyKeyboardRemove())
    #     return "get location"
    if bot.message.text == "Обмен валюты":
        my_keyboard = ReplyKeyboardMarkup([["Ближайшие обменники"], [button_menu]])
        bot.message.reply_text(text=get_html(params="text"), reply_markup=my_keyboard, parse_mode=ParseMode.HTML)
        bot.message.reply_text(text="По нажатию кнопки '<b>Ближайшие обменники</b>' вы увидите курс покупки и продажи ",
                               reply_markup=my_keyboard, parse_mode=ParseMode.HTML)
        return "exchange"


"""Основная развилка по курсу валют"""


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
    receive = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    data = json.loads(receive.text)
    spisok_currency.append([data["Valute"]["USD"]["Name"]])
    letter_code.append([data["Valute"]["USD"]["CharCode"]])
    spisok_currency.append([data["Valute"]["EUR"]["Name"]])
    letter_code.append([data["Valute"]["EUR"]["CharCode"]])
    for valute in data["Valute"]:
        if data["Valute"]["%s" % valute]["Name"] != "Доллар США" and data["Valute"]["%s" % valute]["Name"] != "Евро":
            spisok_currency.append([data["Valute"]["%s" % valute]["Name"]])
            letter_code.append([data["Valute"]["%s" % valute]["CharCode"]])
    if bot.message.text == "Определенная валюта сегодня":
        my_keyboard = ReplyKeyboardMarkup(spisok_currency)
        bot.message.reply_text(text="Выберете валюту чтобы увидеть информацию по ней за сегодня",
                               reply_markup=my_keyboard)
        return "currency statistics"
    if bot.message.text == "Курс валюты в выбранные даты":
        my_keyboard = ReplyKeyboardMarkup(spisok_currency)
        bot.message.reply_text(text="Выберете валюту чтобы увидеть информацию по ней за промежуток времени!",
                               reply_markup=my_keyboard)
        return "date input"
    if bot.message.text == button_menu:
        my_keyboard = ReplyKeyboardMarkup([[button_currency], [button_help, button_end]])
        bot.message.reply_text(text="Вы находитесь в главном меню", reply_markup=my_keyboard)
        return "spisok comand"


"""Статистика за промежуток времени"""


def currency_statistics(bot, update):
    global ind, value
    value = bot.message.text
    receive = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    data = json.loads(receive.text)
    for valute in data["Valute"]:
        if value == data["Valute"]["%s" % valute]["Name"]:
            ind = valute
            continue
    bot.message.reply_text(
        text="Валюта: <b>%s</b>\nСокращенное название: <b>%s</b>\nКоличество: <b>%s</b>\nКурс: <b>%s</b> <i>рублей</i>" % (
            data["Valute"]["%s" % ind]["Name"], data["Valute"]["%s" % ind]["CharCode"],
            data["Valute"]["%s" % ind]["Nominal"],
            data["Valute"]["%s" % ind]["Value"]), parse_mode=ParseMode.HTML)
    my_keyboard = ReplyKeyboardMarkup([["Обмен валюты"], [button_currency], [button_help, button_end]])
    bot.message.reply_text(text="Вы находитесь в главном меню", reply_markup=my_keyboard)
    return "spisok comand"


# Создание диапазона дат
def date_input(bot, update):
    global value
    value = bot.message.text
    bot.message.reply_text(
        text="Введите диапозон дат как на примере:'<b>2020-10-25 2020-11-5</b>'\n'<i>Год-месяц-число Год-месяц-число</i>'\nБез ковычек!!!",
        reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
    return "currency certain statistics"


# Вывод статистики за заданный промежуток времени
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
    try:
        currency_start_date = pd.to_datetime(currency_start_date)  # Преобразование в дату
        currency_end_date = pd.to_datetime(currency_end_date)  # Преобразование в дату
    except ValueError:
        bot.message.reply_text(text="Введенная вами дата не существует или неккоректна\nВведите новые даты")
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
    plt.plot(df["date"], df["value"], lw=1, ls='-', marker='o', markersize=5)  # создание осей
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
    my_keyboard = ReplyKeyboardMarkup([["Обмен валюты"], [button_currency], [button_menu, button_end]])
    bot.message.reply_text(text="Выбери команду", reply_markup=my_keyboard)

    return "spisok comand"


"""Обмен валюты"""


def exchange(bot, update):
    my_keyboard = ReplyKeyboardMarkup([["Курс обменников"], ["Ближайшие обменники"], [button_menu]])
    if bot.message.text == "Курс обменников":
        bot.message.reply_text(text=get_html(params="text"), reply_markup=my_keyboard, parse_mode=ParseMode.HTML)
        bot.message.reply_text(text="Выберите команду!")
        return "exchange"
    if bot.message.text == "Ближайшие обменники":
        bot.message.reply_text(
            text="Чтобы отправить нам геопозицию нажмите на <b>'скрепку'</b>,затем <b>'прикрепить геопозицию'</b>",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML)
        return "get location"


"""Получаем геопозицию пользователя"""


def get_location(bot, update):
    location = bot.message.location
    latitude = location["latitude"]
    longitude = location["longitude"]
    print(latitude, longitude)
    bot.message.reply_text(text="Сейчас подберем ближайшие к вам обменники %s" % bot.message.chat.first_name)
    bot.message.reply_text(text=get_distance(get_html("distance"), "distance", latitude, longitude),
                           parse_mode=ParseMode.HTML,reply_markup=inline_sort())
    return "sort"


"""кнопки с покупкой продажей inline"""


def inline_sort():
    keyboard = [[InlineKeyboardButton("покупка", callback_data="покупка"),
                InlineKeyboardButton("продажа", callback_data="продажа")]]
    return InlineKeyboardMarkup(keyboard)

def inline_sort_callback(bot,update):
    query=bot.callback_query
    data=query.data
    if data=="покупка":
        query.edit_message_text(text="sortiruy daun)))",reply_markup=inline_sort())


def main():  # Основные параметры работы бота(Токен,диалог)
    print("Бот с курсами валют запущен")
    updater = Updater(token=TG_Token, use_context=True)
    start_handler = updater.dispatcher.add_handler(
        ConversationHandler(entry_points=[CommandHandler("start", message_handler)],
                            states={
                                "spisok comand": [
                                    MessageHandler(Filters.regex("/help|/end|Валюты|/menu|Обмен валюты"),
                                                   spisok_comand)],
                                "currency menu": [MessageHandler(
                                    Filters.regex("Определенная валюта сегодня|Курс валюты в выбранные даты|/menu"),
                                    currency_spisok_command)],
                                "currency statistics": [MessageHandler(Filters.text, currency_statistics)],
                                "date input": [MessageHandler(Filters.text, date_input)],
                                "currency certain statistics": [
                                    MessageHandler(Filters.text, currency_certain_statistics)],
                                "get location": [MessageHandler(Filters.location, get_location)],
                                "exchange": [MessageHandler(Filters.regex("Курс обменников|Ближайшие обменники|/menu"),exchange)],
                                 "sort":[CallbackQueryHandler(inline_sort_callback,"покупка")]
                            },
                            fallbacks=[MessageHandler(Filters.text | Filters.video | Filters.document | Filters.photo,
                                                      dontknow)]
                            )

    )
    # inline_keyboard_handler=CallbackQueryHandler(callback=inline_sort_callback,pass_chat_data=True)
    # updater.dispatcher.add_handler(inline_keyboard_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
