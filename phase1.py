from Parser import Parser
from PostController import PostController
from VoteController import VoteController
from TagController import TagController

# setup connection to collections
posts = PostController()
votes = VoteController()
tags = TagController()

# setup parser
parser = Parser()

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()