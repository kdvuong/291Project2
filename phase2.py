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


def main():
    return

if __name__ == "__main__":
    main()