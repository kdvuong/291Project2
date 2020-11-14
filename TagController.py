class TagController:
    def __init__(self, db):
        self.collectionName = 'Tags'
        self.collection = db[self.collectionName]

    def get(self):
        return

    def addMany(self, data):
        self.collection.insert_many(data)
        return

    def delete(self):
        return

    def update(self):
        return

    def getCollectionName(self):
        return self.collectionName


