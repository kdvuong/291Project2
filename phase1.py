from Parser import Parser
from JsonParser import JsonParser
from DbConnection import db
from PostController import PostController
from VoteController import VoteController
from TagController import TagController


# setup connection to collections
posts = PostController(db)
votes = VoteController(db)
tags = TagController(db)

# setup parser
jsonParser = JsonParser()
parser = Parser()

def setup():
    collectionNames = db.list_collection_names()
    if (posts.getCollectionName() in collectionNames):
        db.drop_collection(posts.getCollectionName())

    if (votes.getCollectionName() in collectionNames):
        db.drop_collection(votes.getCollectionName())

    if (votes.getCollectionName() in collectionNames):
        db.drop_collection(tags.getCollectionName())

def buildPostCollection():
    postData = jsonParser.getData("posts.json")["posts"]["row"]
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
    setup()
    buildPostCollection()
    buildTagsCollection()
    buildVotesCollection()
    


if __name__ == "__main__":
    main()
