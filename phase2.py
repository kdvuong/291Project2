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
        totalScore = 0
        for question in questions:
            totalScore += question["Score"]
        
        print("Questions count: {count}".format(count = questionsCount))
        print("Avg score      : {score}".format(score = totalScore/questionsCount))
        
        print("DONE DONE DONE DONE------------")
    else:
        print("No user id provided")

    return

if __name__ == "__main__":
    main()