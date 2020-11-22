import uuid

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

    def addTags(self, tags):
        for tag in tags:
            existingTag = self.collection.find_one({"TagName": tag})
            if (existingTag == None):
                self.collection.insert_one({
                    "Id": str(uuid.uuid4()),
                    "Count": 1
                })
            else:
                self.collection.update_one({"TagName": tag}, {"$inc": {"Count": 1}})


