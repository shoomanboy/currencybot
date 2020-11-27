from pymongo import MongoClient
import pymongo
import dateutil
from dateutil import parser
import datetime
TG_Token = "1221399834:AAEpvx0WQ-42sW3O0LHgMnJXLGabAm7JgFI"
MONGODB_LINK = "mongodb+srv://shoomaher:7598621zhora@telegrambot.fls8z.mongodb.net/telegrambot?retryWrites=true&w=majority"
COLLECTION = "telegrambot"
MONGODB = "telegrambotcurrency"
mdb = MongoClient(MONGODB_LINK)[COLLECTION][MONGODB]  # переменная для работы с БД
id_name = 1
"""Создание даты в бд """
# text="2020-10-15"
# text1="2020-10-10"
# text2="2020-10-17"
# print(text)
# text = dateutil.parser.parse(text).isoformat()
# text1=dateutil.parser.parse(text1).isoformat()
# text2=dateutil.parser.parse(text2).isoformat()
# print(text)
# text=datetime.datetime.strptime(text,"%Y-%m-%dT%H:%M:%S").isoformat()
#
# result=mdb.update_one({"_id":id_name},{"$push":{"statistics.date":text}})

# for x in mdb.find({"_id":id_name},{"statistics.date"}).sort("statistics.date"):
#     print(x)

