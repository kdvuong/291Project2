class PostController:
    def __init__(self, db):
        self.collectionName = 'Posts'
        self.collection = db[self.collectionName]

    def get(self):
        return self.collection.find()

    def addOne(self, postId, date, userId, body, title):
        if (userId != ""): # with userID
            NewPost = {
                "Id": postId,
                "PostTypeId": 1,
                "CreationDate": date,
                "Score": 0,
                "ViewCount": 0,
                "Body": body,
                "OwnerUserId": userId,
                "AnswerCount": 0,
                "CommentCount": 0,
                "FavoriteCount": 0,
                "ContentLicense": "CC BY-SA 2.5"
            }
        else: # anonymous user
            NewPost = {
                "Id": postId,
                "PostTypeId": 1,
                "CreationDate": date,
                "Score": 0,
                "ViewCount": 0,
                "Body": body,
                "AnswerCount": 0,
                "CommentCount": 0,
                "FavoriteCount": 0,
                "ContentLicense": "CC BY-SA 2.5"
            }
        # Insert Data
        self.collection.insert_one(NewPost)

    
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