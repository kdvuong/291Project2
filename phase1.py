from Parser import Parser
from JsonParser import JsonParser
from DbConnection import getDb
from PostController import PostController
from VoteController import VoteController
from TagController import TagController

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

def setupCollections():
    collectionNames = db.list_collection_names()
    if (posts.getCollectionName() in collectionNames):
        db.drop_collection(posts.getCollectionName())

    if (votes.getCollectionName() in collectionNames):
        db.drop_collection(votes.getCollectionName())

    if (votes.getCollectionName() in collectionNames):
        db.drop_collection(tags.getCollectionName())

def buildPostCollection():
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

    posts.addMany(postData)

def buildTagsCollection():
    data = jsonParser.getData("Tags.json")['tags']['row']
    tags.addMany(data)

def buildVotesCollection():
    data = jsonParser.getData("Votes.json")['votes']['row']
    votes.addMany(data)

def main():
    setupCollections()
    buildPostCollection()
    buildTagsCollection()
    buildVotesCollection()
    


if __name__ == "__main__":
    main()
