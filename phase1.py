from Parser import Parser
from JsonParser import JsonParser
from PostController import PostController
from VoteController import VoteController
from TagController import TagController

# setup connection to collections
posts = PostController()
votes = VoteController()
tags = TagController()

# setup parser
jsonParser = JsonParser()
parser = Parser()

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

def main():
    buildPostCollection()
    


if __name__ == "__main__":
    main()