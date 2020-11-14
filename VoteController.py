from DbConnection import db
from JsonParser import JsonParser

class VoteController:
    def __init__(self):
        self.collection = db['Votes']

    def getAllData(self):
        return self.collection.find()

    def getData(self, id):
        return self.collection.find({"VoteTypeId": {"$eq": id}})

    def addMany(self, data):
        self.collection.insert_many(data)

    def delete(self):
        return

    def update(self):
        return

# parser
parser = JsonParser()
data = parser.getData("Votes.json")

# add data
v = VoteController()
v.add(data['votes']['row'])

# data = v.getAllData()
data = list(v.getData("1"))
for docs in data:
    print(data)