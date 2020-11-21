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
    userId = input("Enter user id (optional): ")
    if (userId != ""):
        questions = posts.getQuestions(userId)
        questionsCount = questions.count()
        for question in questions:
            print(question)
    else:
        print("No user id provided")

    return

if __name__ == "__main__":
    main()