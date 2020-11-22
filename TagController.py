import uuid


# Class to handle tag action
class TagController:
    def __init__(self, db):
        self.collectionName = 'Tags'
        self.collection = db[self.collectionName]

    # function to add the data to collection
    def addMany(self, data):
        self.collection.insert_many(data)
        return

    # function to return the collection name
    def getCollectionName(self):
        return self.collectionName

    # function to record the added tag to the database
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


