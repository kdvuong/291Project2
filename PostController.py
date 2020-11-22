from datetime import datetime
import uuid
from Parser import Parser

parser = Parser()

# Class to handle post action
class PostController:
    def __init__(self, db):
        self.collectionName = 'Posts'
        self.collection = db[self.collectionName]

    # function to return all the post
    def get(self):
        return self.collection.find()

    # function record a new post to database
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

    # function to add many post to database
    def addMany(self, posts):
        self.collection.insert_many(posts)

    # function to return collection name
    def getCollectionName(self):
        return self.collectionName
    
    # function to create index for post
    def createIndex(self, fieldName):
        self.collection.create_index([(fieldName, -1)])

    # function to return question posts
    def getQuestions(self, userId):
        return self.collection.find({
            "OwnerUserId": userId,
            "PostTypeId": "1"
        })

    # function to return answer posts
    def getAnswers(self, userId):
        return self.collection.find({
            "OwnerUserId": userId,
            "PostTypeId": "2"
        })

    # function to return question post by keywords
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

    # function to handle view count
    def increaseViewCount(self, id):
        self.collection.update_one({ "_id": id}, {"$inc": { "ViewCount": 1}})

    # function to record an new answer post to database
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
        self.collection.update_one({"Id": parentId}, {"$inc": {"AnswerCount": 1}})

    # function to return answer posts by keywords
    def getAnswersByQuestionId(self, qid):
        return self.collection.find({"ParentId": qid, "PostTypeId": "2"})
    
    # function to handle score count
    def increaseScore(self, id):
        self.collection.update_one({ "_id": id}, {"$inc": { "Score": 1}})
