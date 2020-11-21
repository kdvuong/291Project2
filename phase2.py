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
        questions = list(posts.getQuestions(userId))
        questionsCount = len(questions)
        totalScore = 0
        for question in questions:
            totalScore += question["Score"]

        avgScore = 0
        if (questionsCount > 0):
            avgScore = totalScore/questionsCount
        
        print("Questions count: {count}".format(count = questionsCount))
        print("Avg score      : {score}".format(score = avgScore))
        
        print("DONE DONE DONE DONE------------")
    else:
        print("No user id provided")

    return

if __name__ == "__main__":
    main()