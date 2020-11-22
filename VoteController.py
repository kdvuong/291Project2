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
    
    def getByUserId(self, userId):
        return self.collection.find({
            "UserId": userId
        })
    
    def vote(self, userId, postId):
        vote = {
            "Id": str(uuid.uuid4()),
            "PostId": postId,
            "VoteTypeId": "2",
            "CreationDate": datetime.now(),
        }

        if (userId != ""):
            vote["UserId"] = userId

        self.collection.insert_one(vote)
    
    def isVoted(self, userId, postId):
        votes = list(self.collection.find_one({
            "OwnerUserId": userId
            "Id": userId
        }))
        if (len(votes) > 0):
            return True
        else: return False

    
