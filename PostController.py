from datetime import datetime
import uuid
from Parser import Parser

parser = Parser()

class PostController:
    def __init__(self, db):
        self.collectionName = 'Posts'
        self.collection = db[self.collectionName]

    def get(self):
        return self.collection.find()

    def postQuestion(self, userId, body, title, tags):
        newPost = {
            "Id": str(uuid.uuid4()),
            "PostTypeId": "1",
            "CreationDate": datetime.now(),
            "Score": 0,
            "ViewCount": 0,
            "Body": body,
            "Title": title,
            "AnswerCount": 0,
            "CommentCount": 0,
            "FavoriteCount": 0,
            "ContentLicense": "CC BY-SA 2.5",
            "Terms": parser.parseTitleAndBody({"title": title, "body": body})
        }

        if (userId != ""): # with userID
            newPost["OwnerUserId"] = userId

        if (len(tags) > 0):
            newPost["Tags"] = tags

        # Insert Data
        self.collection.insert_one(newPost)

    
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

    def getQuestionsByKeywords(self, keywords):
        return self.collection.find({
            "PostTypeId": "1",
            "$or": [
                {
                    "Terms": {
                        "$in": keywords
                    }
                },
                {
                    "Tags": {
                        "$in": keywords
                    }
                }
            ]
        })

    def increaseViewCount(self, id):
        self.collection.update_one({ "_id": id}, {"$inc": { "ViewCount": 1}})

    def postAnswer(self, userId, parentId, body):
        answer = {
            "Id": str(uuid.uuid4()),
            "PostTypeId": "2",
            "ParentId": parentId,
            "CreationDate": datetime.now(),
            "Score": 0,
            "Body": body,
            "CommentCount": 0,
            "ContentLicense": "CC BY-SA 2.5",
            "Terms": parser.parseTitleAndBody({"title": "", "body": body})
        }

        print(answer["Id"])

        if (userId != ""):
            answer["OwnerUserId"] = userId

        self.collection.insert_one(answer)
    
    
    def increateScore(self, post):
        post["Score"] += 1
