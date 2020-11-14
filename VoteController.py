class VoteController:
    def __init__(self, db):
        self.collectionName = 'Votes'
        self.collection = db[self.collectionName]

    def getAll(self):
        return self.collection.find()

    def get(self, id):
        return self.collection.find({"Id": {"$eq": id}})

    def addMany(self, data):
        self.collection.insert_many(data)

    def delete(self):
        return

    def update(self):
        return

    def getCollectionName(self):
        return self.collectionName
