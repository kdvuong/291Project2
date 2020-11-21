class PostController:
    def __init__(self, db):
        self.collectionName = 'Posts'
        self.collection = db[self.collectionName]

    def get(self):
        return

    def add(self, post):
        return
    
    def addMany(self, posts):
        self.collection.insert_many(posts)
    def delete(self):
        return

    def update(self):
        return

    def getCollectionName(self):
        return self.collectionName
    
    def createIndex(self, fieldName):
        self.collection.create_index([(fieldName, -1)])

    def getQuestions(self, userId):
        return self.collection.find({
            "OwnerUserId": userId,
            "PostTypeId": "1"
        })

    def getAnswers(self, userId):
        return self.collection.find({
            "OwnerUserId": userId,
            "PostTypeId": "2"
        })