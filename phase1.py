from Parser import Parser
from JsonParser import JsonParser
from DbConnection import getDb
from PostController import PostController
from VoteController import VoteController
from TagController import TagController
import time

# setup db
db = None
try:
    db = getDb()
except Exception as err:
    print(err.args[0])
    exit()

# setup connection to collections
posts = PostController(db)
votes = VoteController(db)
tags = TagController(db)

# setup parser
jsonParser = JsonParser()
parser = Parser()

# function to handle setting up collections
def setupCollections():
    collectionNames = db.list_collection_names()
    if (posts.getCollectionName() in collectionNames):
        db.drop_collection(posts.getCollectionName())

    if (votes.getCollectionName() in collectionNames):
        db.drop_collection(votes.getCollectionName())

    if (votes.getCollectionName() in collectionNames):
        db.drop_collection(tags.getCollectionName())
    
# function to build post collection
def buildPostCollection():
    print("Building post collection")
    start = time.time()

    postData = jsonParser.getData("Posts.json")["posts"]["row"]
    for data in postData:
        titleAndBody = {"title": "", "body": ""}
        if "Title" in data:
            titleAndBody["title"] = data["Title"]
        
        if "Body" in data:
            titleAndBody["body"] = data["Body"]

        data["Terms"] = parser.parseTitleAndBody(titleAndBody)

        if "Tags" in data:
            data["Tags"] = parser.parseTags(data["Tags"])

    posts.createIndex("Terms")
    posts.addMany(postData)

    end = time.time()
    print("Done. Time elapsed: {elapsed}".format(elapsed = end - start))

# function to build tag collection
def buildTagsCollection():
    print("Building tags collection")
    start = time.time()

    data = jsonParser.getData("Tags.json")['tags']['row']
    tags.addMany(data)

    end = time.time()
    print("Done. Time elapsed: {elapsed}".format(elapsed = end - start))

# function to build vote collection
def buildVotesCollection():
    print("Building votes collection")
    start = time.time()

    data = jsonParser.getData("Votes.json")['votes']['row']
    votes.addMany(data)

    end = time.time()
    print("Done. Time elapsed: {elapsed}".format(elapsed = end - start))

def main():
    start = time.time()

    # Set up collections
    setupCollections()
    buildPostCollection()
    buildTagsCollection()
    buildVotesCollection()
    
    end = time.time()
    print("Successfully built all collections. Total time elapsed: {elapsed}".format(elapsed = end - start))

if __name__ == "__main__":
    main()
