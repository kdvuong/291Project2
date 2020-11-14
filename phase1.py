import pymongo
from pymongo import MongoClient
from Parser import Parser

cluster = MongoClient("mongodb+srv://khang:Khang99!@cluster0.27zhi.mongodb.net/291db?retryWrites=true&w=majority")
db = cluster["291db"]
posts = db["posts"]
tags = db["tags"]
votes = db["votes"]

