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

# mdb.update_one({"_id":2},{"$set":{"user_id":{"853615222":2}}})
result=mdb.find_one({"_id":2,"user_id.853615222":{"$exists":True}})
print(result)