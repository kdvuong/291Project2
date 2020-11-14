import pymongo
from pymongo import MongoClient
from Parser import Parser

dbName = "291db"
cluster = MongoClient("mongodb+srv://khang:Khang99!@cluster0.27zhi.mongodb.net/{name}?retryWrites=true&w=majority".format(name = dbName))
db = cluster[dbName]