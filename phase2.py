from DbConnection import getDb
from PostController import PostController
from VoteController import VoteController
from TagController import TagController
from datetime import date
import uuid

# constants
ACTION_OPTIONS = """-----------------------------------
Choose the following option:
-----------------------------------
1. POST (post a question)
2. SEARCH (search for a post)
3. LOGOUT (log out)
------------------------------------
What do you want to do? (number or text): """


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

def getCountAndAvgScore(l):
    count = len(l)
    avgScore = 0

    if (count > 0):
        totalScore = 0
        for item in l:
            totalScore += int(item["Score"])
        avgScore = totalScore/count
    
    return (count, avgScore)


def main():
    userId = input("Enter user id (optional): ")
    if (userId != ""):
        questions = list(posts.getQuestions(userId))
        answers = list(posts.getAnswers(userId))
        voteCount = len(list(votes.getByUserId(userId)))

        questionCount, qAvgScore = getCountAndAvgScore(questions)
        answerCount, aAvgScore = getCountAndAvgScore(answers)
        
        print("Questions count    : {count}".format(count = questionCount))
        print("Questions avg score: {score}".format(score = qAvgScore))
        print("Answers count      : {count}".format(count = answerCount))
        print("Answers avg score  : {score}".format(score = aAvgScore))
        print("Votes casted       : {voteCount}".format(voteCount = voteCount))
        
        print("DONE DONE DONE DONE------------")
    else:
        print("No user id provided")

    while (1):
        actions = input(ACTION_OPTIONS)
        if (actions == 1):
            title = input("Enter a title: ")
            body = input("Enter a body: ")
            tags = input("Enter a tag (optional): ")
            postId = uuid.uuid4()
            date = date.today()
            if (tags != ""):
                posts.update({"Id": postId}, {"$set": {"Tags": "<{tag}>"}.format(tag = tags)})
            else:
                continue

    return

if __name__ == "__main__":
    main()