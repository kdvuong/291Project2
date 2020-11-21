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
    else:
        print("No user id provided")

    while (True):
        action = input("Choose an action: ")
        if (action == "1"):
             title = input("Enter a title: ")
            body = input("Enter a body: ")
            tags = input("Enter a tag (optional): ")
            postId = uuid.uuid4()
            date = date.today()
            if (tags != ""):
                posts.update({"Id": postId}, {"$set": {"Tags": "<{tag}>"}.format(tag = tags)})
            else:
                continue
        elif (action == "2"):
            keywords = input("Enter keywords to search: ").lower().split(" ")
            searchResult = list(posts.getQuestionsByKeywords(keywords))
            if (len(searchResult) > 0):
                print("Id | Title | Creation Date | Score | Answer Count")
                for index, item in enumerate(searchResult):
                    print("{index} | {id} | {title} | {date} | {score} | {answerCount}".format(
                        index = index,
                        id = item["Id"],
                        title = item["Title"],
                        date = item["CreationDate"],
                        score = item["Score"],
                        answerCount = item["AnswerCount"]
                    ))
                
                chosenIndex = int(input("Choose a question by index: "))
                if (chosenIndex < len(searchResult) and chosenIndex >= 0):
                    chosenQuestion = searchResult[chosenIndex]
                    columns = chosenQuestion.keys()
                    for col in columns:
                        if (col != "_id"):
                            print("{col}: {val}".format(col = col, val = chosenQuestion[col]))
                    posts.increaseViewCount(chosenQuestion["_id"])

                    while (True):
                        print("Available actions:")
                        print("1. answer - post an answer for this question")
                        print("2. list   - list all answers")
                        print("3. vote   - cast a vote to this question")
                        print("4. back   - go back")
                        questionAction = input("Choose an action (text or number): ").lower()
                        if (questionAction == "1" or questionAction == "answer"):
                            # answer
                            continue
                        elif (questionAction == "2" or questionAction == "list"):
                            # list answers
                            continue
                        elif (questionAction == "3" or questionAction == "vote"):
                            # vote
                            continue
                        elif (questionAction == "4" or questionAction == "back"):
                            break
                        else:
                            print("ERROR: invalid action. Choose again.")
                else:
                    print("ERROR: invalid index. Choose again.")
            else:
                print("No questions found with provided keywords: {keywords}".format(keywords = keywords))
        elif (action == "exit"):
            print("exiting...")
            break

    return

if __name__ == "__main__":
    main()