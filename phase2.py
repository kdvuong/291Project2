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
        if (action == "2"):
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
                            print("{col}: {val}", col = col, val = chosenQuestion[col])

            else:
                print("No questions found with provided keywords: {keywords}".format(keywords = keywords))
        elif (action == "exit"):
            print("exiting...")
            break

    return

if __name__ == "__main__":
    main()