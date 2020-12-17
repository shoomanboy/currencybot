from pymongo import MongoClient
import pymongo
import dateutil
from dateutil import parser
import datetime
TG_Token = "TOKEN"
MONGODB_LINK = "MONGODBLINK"
COLLECTION = "telegrambot"
MONGODB = "telegrambotcurrency"
mdb = MongoClient(MONGODB_LINK)[COLLECTION][MONGODB]  # переменная для работы с БД
id_name = 1

