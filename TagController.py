from DbConnection import db
import json
from JsonParser import JsonParser

class TagController:
    def __init__(self):
        self.collection = db['Tags']
    def get():
        return

    def addMany(self, data):
        self.collection.insert_many(data)
        return

    def delete(self):
        return

    def update():
        return

j = JsonParser()
data = j.getData("Tags.json")['tags']['row']

tag = TagController()
tag.addMany(data)

