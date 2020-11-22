from datetime import datetime
import uuid

# Class to handle vote action
class VoteController:
    def __init__(self, db):
        self.collectionName = 'Votes'
        self.collection = db[self.collectionName]

    # function to return all the votes in the collection
    def getAll(self):
        return self.collection.find()

    # function to return a vote by Id
    def get(self, id):
        return self.collection.find({"Id": {"$eq": id}})

    # function to add many data to the database
    def addMany(self, data):
        self.collection.insert_many(data)

    # function to return the collection name
    def getCollectionName(self):
        return self.collectionName
    
    # function to return the vote by userId
    def getByUserId(self, userId):
        return self.collection.find({
            "UserId": userId
        })
    
    # function to record the new vote to the database
    def addVote(self, userId, postId):
        vote = {
            "Id": str(uuid.uuid4()),
            "PostId": postId,
            "VoteTypeId": "2",
            "CreationDate": datetime.now(),
        }

        if (userId != ""):
            vote["UserId"] = userId

        self.collection.insert_one(vote)
    
    # function to check if the post is voted or not
    def isVoted(self, userId, postId):
        vote = self.collection.find_one({
            "UserId": userId,
            "PostId": postId
        })

        return vote != None

    
