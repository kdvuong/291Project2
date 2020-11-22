from DbConnection import getDb
from PostController import PostController
from VoteController import VoteController
from TagController import TagController


# constants
MAIN_ACTION_PROMPT = """Available actions:
1. post   - post a question
2. search - search for questions by keywords
3. exit   - exit program"""

QUESTION_ACTION_PROMPT = """Available actions:
1. answer - post an answer for this question
2. list   - list all answers
3. vote   - cast a vote to this question
4. back   - go back to search list"""

ANSWER_ACTION_PROMPT = """Available action: 
1. vote - cast a vote for this answer
2. back - go back to answer list"""

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

def printSummary(questionCount, qAvgScore, answerCount, aAvgScore, voteCount):
    print("Questions count    : {count}".format(count = questionCount))
    print("Questions avg score: {score}".format(score = qAvgScore))
    print("Answers count      : {count}".format(count = answerCount))
    print("Answers avg score  : {score}".format(score = aAvgScore))
    print("Votes casted       : {voteCount}".format(voteCount = voteCount))

def printSearchResult(searchResult):
    print("Id | Title | Creation Date | Score | Answer Count")
    for item in searchResult:
        print("{id} | {title} | {date} | {score} | {answerCount}".format(
            id = item["Id"],
            title = item["Title"],
            date = item["CreationDate"],
            score = item["Score"],
            answerCount = item["AnswerCount"]
        ))

def getItemFromListById(id, itemList):
    for item in itemList:
        if (item["Id"] == id):
            return item
    
    return None

def printDocument(doc):
    columns = doc.keys()
    for col in columns:
        if (col != "_id"):
            print("{col}: {val}".format(col = col, val = doc[col]))

def moveAcceptedAnswerToFront(answers, acceptedAnswerId):
    if (answers[0]["Id"] != acceptedAnswerId):
        for index, answer in enumerate(answers):
            if (answer["Id"] == acceptedAnswerId):
                acceptedAnswer = answers.pop(index)
                answers.insert(0, acceptedAnswer)
                break
    else:
        return

def truncate(s, x):
    if (len(s) > x):
        return s[0:x] + "..."
    else:
        return s

def printAnswerList(answers, hasAcceptedAnswer):
    print("Id | Body | Creation Date | Score ")
    for index, answer in enumerate(answers):
        print("{id} | {body} | {date} | {score} {star}".format(
            id = answer["Id"],
            body = truncate(answer["Body"], 80),
            date = answer["CreationDate"],
            score = answer["Score"],
            star = "*" if hasAcceptedAnswer and index == 0 else ""
        ))

def votePost(userId, post):
    if (userId == ""):
        votes.addVote(userId, post["Id"])
        posts.increaseScore(post["_id"])
        print("Vote success")
    else:
        if not votes.isVoted(userId, post["Id"]):
            votes.addVote(userId, post["Id"])
            posts.increaseScore(post["_id"])
        else:
            print("You already voted this post")

def main():
    userId = input("Enter user id (optional): ")
    if (userId != ""):
        questions = list(posts.getQuestions(userId))
        answers = list(posts.getAnswers(userId))
        voteCount = len(list(votes.getByUserId(userId)))

        questionCount, qAvgScore = getCountAndAvgScore(questions)
        answerCount, aAvgScore = getCountAndAvgScore(answers)
        
        printSummary(questionCount, qAvgScore, answerCount, aAvgScore, voteCount)
    else:
        print("No user id provided")

    while (True):
        print(MAIN_ACTION_PROMPT)
        action = input("Choose an action (number or text): ").lower()

        if (action == "1" or action == "post"):
            title = input("Enter a title: ")
            if (len(title) == 0):
                print("ERROR: post title cannot be empty")
                continue

            body = input("Enter a body: ")
            if (len(body) == 0):
                print("ERROR: post body cannot be empty")
                continue

            tagList = input("Enter tags (optional): ").lower().strip()
            
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
                printSearchResult(searchResult)
                
                chosenQid = input("Choose a question id: ")
                chosenQuestion = getItemFromListById(chosenQid, searchResult)
                
                if (chosenQuestion != None):
                    printDocument(chosenQuestion)
                    posts.increaseViewCount(chosenQuestion["_id"])

                    while (True):
                        print(QUESTION_ACTION_PROMPT)
                        questionAction = input("Choose an action (text or number): ").lower()

                        if (questionAction == "1" or questionAction == "answer"):
                            answerBody = input("Answer body: ")
                            if (len(answerBody) == 0):
                                print("ERROR: answer body cannot be empty")
                                continue
                            posts.postAnswer(userId, chosenQuestion["Id"], answerBody)
                        elif (questionAction == "2" or questionAction == "list"):
                            answers = list(posts.getAnswersByQuestionId(chosenQuestion["Id"]))
                            if (len(answers) > 0):
                                hasAcceptedAnswer = "AcceptedAnswerId" in chosenQuestion
                                if hasAcceptedAnswer:
                                    moveAcceptedAnswerToFront(answers, chosenQuestion["AcceptedAnswerId"])
                                
                                printAnswerList(answers, hasAcceptedAnswer)

                                chosenAid = input("Choose an answer id: ")
                                chosenAnswer = getItemFromListById(chosenAid, answers)

                                if (chosenAnswer != None):
                                    printDocument(chosenAnswer)
                                    
                                    while (True):
                                        print(ANSWER_ACTION_PROMPT)
                                        answerAction = input("Choose an action: ").lower()

                                        if (answerAction == "1" or answerAction == "vote"):
                                            votePost(userId, chosenAnswer)
                                        elif (answerAction == "2" or answerAction == "back"):
                                            break
                                        else:
                                            print("ERROR: invalid action. Choose again.")
                                else:
                                    print("ERROR: invalid answer id. Choose again.")
                            else:
                                print("Question has no answer.")
                        elif (questionAction == "3" or questionAction == "vote"):
                            votePost(userId, chosenQuestion)
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