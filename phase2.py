from DbConnection import getDb
from PostController import PostController
from VoteController import VoteController
from TagController import TagController


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
        print("Available actions:")
        print("1. post   - post a question")
        print("2. search - search for questions by keywords")
        print("3. exit   - exit program")

        action = input("Choose an action (number or text): ").lower()

        if (action == "1" or action == "post"):
            title = input("Enter a title: ")
            body = input("Enter a body: ")
            tagList = input("Enter a tag (optional): ").lower().strip()
            
            if (tagList != ""):
                tagList = tagList.split(" ")
                tags.addTags(tagList)
            else:
                tagList = []
            
            posts.postQuestion(userId, body, title, tagList)
        elif (action == "2" or action == "search"):
            keywords = input("Enter keywords to search: ").lower().split(" ")
            searchResult = list(posts.getQuestionsByKeywords(keywords))
            if (len(searchResult) > 0):
                print("Id | Title | Creation Date | Score | Answer Count")
                for item in searchResult:
                    print("{id} | {title} | {date} | {score} | {answerCount}".format(
                        id = item["Id"],
                        title = item["Title"],
                        date = item["CreationDate"],
                        score = item["Score"],
                        answerCount = item["AnswerCount"]
                    ))
                
                chosenQid = input("Choose a question id: ")
                chosenQuestion = None
                for question in searchResult:
                    if (question["Id"] == chosenQid):
                        chosenQuestion = question
                        break
                
                if (chosenQuestion != None):
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
                        print("4. back   - go back to search list")
                        questionAction = input("Choose an action (text or number): ").lower()
                        if (questionAction == "1" or questionAction == "answer"):
                            answerBody = input("Answer body: ")
                            posts.postAnswer(userId, chosenQuestion["Id"], answerBody)
                        elif (questionAction == "2" or questionAction == "list"):
                            answers = list(posts.getAnswersByQuestionId(chosenQuestion["Id"]))
                            if (len(answers) > 0):
                                if "AcceptedAnswerId" in chosenQuestion:
                                    for index, answer in enumerate(answers):
                                        if (answer["Id"] == chosenQuestion["AcceptedAnswerId"]):
                                            acceptedAnswer = answers.pop(index)
                                            answers.insert(0, acceptedAnswer)
                                
                                print("Id | Body | Creation Date | Score ")
                                for answer in answers:
                                    star = ""
                                    if "AcceptedAnswerId" in chosenQuestion:
                                        if (answer["Id"] == chosenQuestion["AcceptedAnswerId"]):
                                            star = "*"

                                    answerBody = answer["Body"]
                                    if (len(answerBody) > 80):
                                        answerBody = answerBody[0:80] + "..."

                                    print("{id} | {body} | {date} | {score} {star}".format(
                                        id = answer["Id"],
                                        body = answerBody,
                                        date = answer["CreationDate"],
                                        score = answer["Score"],
                                        star = star
                                    ))
                                chosenAid = input("Choose an answer id: ")
                                chosenAnswer = None

                                for answer in answers:
                                    if (answer["Id"] == chosenAid):
                                        chosenAnswer = answer

                                if (chosenAnswer != None):
                                    answerCols = chosenAnswer.keys()
                                    for col in answerCols:
                                        if (col != "_id"):
                                            print("{col}: {val}".format(col = col, val = chosenAnswer[col]))
                                    
                                    while (True):
                                        print("Available action: ")
                                        print("1. vote - cast a vote for this answer")
                                        print("2. back - go back to answer list")
                                        answerAction = input("Choose an action: ").lower()

                                        if (answerAction == "1" or answerAction == "vote"):
                                            if (userId == ""):
                                                votes.addVote(userId, chosenAnswer["Id"])
                                                posts.increaseScore(chosenAnswer["_id"])
                                                print("Vote success")
                                            else:
                                                if not votes.isVoted(userId, chosenAnswer["Id"]):
                                                    votes.addVote(userId, chosenAnswer["Id"])
                                                    posts.increaseScore(chosenAnswer["_id"])
                                                else:
                                                    print("You already voted this post")
                                        elif (answerAction == "2" or answerAction == "back"):
                                            break
                                        else:
                                            print("ERROR: invalid action. Choose again.")
                                else:
                                    print("ERROR: invalid answer id. Choose again.")
                            else:
                                print("Question has no answer.")

                        elif (questionAction == "3" or questionAction == "vote"):
                            if (userId == ""):
                                votes.addVote(userId, chosenQuestion["Id"])
                                posts.increaseScore(chosenQuestion["_id"])
                                print("Vote success")
                            else:
                                if not votes.isVoted(userId, chosenQuestion["Id"]):
                                    votes.addVote(userId, chosenQuestion["Id"])
                                    posts.increaseScore(chosenQuestion["_id"])
                                else:
                                    print("You already voted this post")
                        elif (questionAction == "4" or questionAction == "back"):
                            break
                        else:
                            print("ERROR: invalid action. Choose again.")
                else:
                    print("ERROR: invalid question id. Choose again.")
            else:
                print("No questions found with provided keywords: {keywords}".format(keywords = keywords))
        elif (action == "3" or action == "exit"):
            print("exiting...")
            break

    return

if __name__ == "__main__":
    main()