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
4. back   - go back to main"""

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

# function to return the count and average Score
def getCountAndAvgScore(l):
    count = len(l)
    avgScore = 0

    if (count > 0):
        totalScore = 0
        for item in l:
            totalScore += int(item["Score"])
        avgScore = totalScore/count
    
    return (count, avgScore)

# function to print out the profile summary of the userId
def printSummary(questionCount, qAvgScore, answerCount, aAvgScore, voteCount):
    print("Questions count    : {count}".format(count = questionCount))
    print("Questions avg score: {score}".format(score = qAvgScore))
    print("Answers count      : {count}".format(count = answerCount))
    print("Answers avg score  : {score}".format(score = aAvgScore))
    print("Votes casted       : {voteCount}".format(voteCount = voteCount))

# function to print out the search result
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

# function to return the item from the list by id
def getItemFromListById(id, itemList):
    for item in itemList:
        if (item["Id"] == id):
            return item
    
    return None

# function to print out the document
def printDocument(doc):
    columns = doc.keys()
    for col in columns:
        if (col != "_id"):
            print("{col}: {val}".format(col = col, val = doc[col]))

# function to move the accepted answer to the front of the list
def moveAcceptedAnswerToFront(answers, acceptedAnswerId):
    if (answers[0]["Id"] != acceptedAnswerId):
        for index, answer in enumerate(answers):
            if (answer["Id"] == acceptedAnswerId):
                acceptedAnswer = answers.pop(index)
                answers.insert(0, acceptedAnswer)
                break
    else:
        return

# function to handle truncating
def truncate(s, x):
    if (len(s) > x):
        return s[0:x] + "..."
    else:
        return s

# function to print out the answer list
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

# function to handle voting a post
def votePost(userId, post):
    if (userId == ""):
        votes.addVote(userId, post["Id"])
        posts.increaseScore(post["_id"])
        print("Vote success")
    else:
        if not votes.isVoted(userId, post["Id"]):
            votes.addVote(userId, post["Id"])
            posts.increaseScore(post["_id"])
            print("Vote success")
        else:
            print("You already voted this post")

def main():
    userId = input("Enter user id (optional): ") # userID
    if (userId != ""):
        questions = list(posts.getQuestions(userId))
        answers = list(posts.getAnswers(userId))
        voteCount = len(list(votes.getByUserId(userId)))

        questionCount, qAvgScore = getCountAndAvgScore(questions)
        answerCount, aAvgScore = getCountAndAvgScore(answers)
        
        printSummary(questionCount, qAvgScore, answerCount, aAvgScore, voteCount)
    else:
        print("No user id provided")

    while (True): # while loop
        print(MAIN_ACTION_PROMPT) # print out the prompt
        action = input("Choose an action (number or text): ").lower()

        if (action == "1" or action == "post"): # post a question
            title = input("Enter a title: ")
            if (len(title) == 0): # not allow empty title
                print("ERROR: post title cannot be empty")
                continue

            body = input("Enter a body: ")
            if (len(body) == 0): # not allow empty body
                print("ERROR: post body cannot be empty")
                continue

            tagList = input("Enter tags (optional): ").lower().strip()
            
            if (tagList != ""): # choose to give tag in the list
                tagList = tagList.split(" ")
                tags.addTags(tagList)
            else: # zero tag
                tagList = []
            
            posts.postQuestion(userId, body, title, tagList)
        elif (action == "2" or action == "search"): # search a post
            keywords = input("Enter keywords to search: ").lower().split(" ") # keyword to search
            searchResult = list(posts.getQuestionsByKeywords(keywords))
            if (len(searchResult) > 0):
                printSearchResult(searchResult)
                
                chosenQid = input("Choose a question id: ") # choose a question
                chosenQuestion = getItemFromListById(chosenQid, searchResult)
                
                if (chosenQuestion != None):
                    printDocument(chosenQuestion)
                    posts.increaseViewCount(chosenQuestion["_id"]) # increase view count

                    while (True):
                        print(QUESTION_ACTION_PROMPT) # prompt the option for the question post
                        questionAction = input("Choose an action (text or number): ").lower()

                        if (questionAction == "1" or questionAction == "answer"): # answer the question
                            answerBody = input("Answer body: ")
                            if (len(answerBody) == 0): # empty body not allowed
                                print("ERROR: answer body cannot be empty")
                                continue
                            posts.postAnswer(userId, chosenQuestion["Id"], answerBody)
                        elif (questionAction == "2" or questionAction == "list"): # list out the answers 
                            answers = list(posts.getAnswersByQuestionId(chosenQuestion["Id"]))
                            if (len(answers) > 0):
                                hasAcceptedAnswer = "AcceptedAnswerId" in chosenQuestion
                                if hasAcceptedAnswer: # accepted answer
                                    moveAcceptedAnswerToFront(answers, chosenQuestion["AcceptedAnswerId"])
                                
                                printAnswerList(answers, hasAcceptedAnswer)

                                chosenAid = input("Choose an answer id: ") # choose an answer
                                chosenAnswer = getItemFromListById(chosenAid, answers)

                                if (chosenAnswer != None):
                                    printDocument(chosenAnswer)
                                    
                                    while (True):
                                        print(ANSWER_ACTION_PROMPT) # prompt the option for answers post
                                        answerAction = input("Choose an action: ").lower()

                                        if (answerAction == "1" or answerAction == "vote"): # vote the answer post
                                            votePost(userId, chosenAnswer)
                                        elif (answerAction == "2" or answerAction == "back"): # go back to prev menu
                                            break
                                        else:
                                            print("ERROR: invalid action. Choose again.")
                                else:
                                    print("ERROR: invalid answer id. Choose again.")
                            else:
                                print("Question has no answer.") 
                        elif (questionAction == "3" or questionAction == "vote"): # vote the question post
                            votePost(userId, chosenQuestion)
                        elif (questionAction == "4" or questionAction == "back"): # go back to previous menu
                            break
                        else:
                            print("ERROR: invalid action. Choose again.")
                else:
                    print("ERROR: invalid question id. Choose again.")
            else:
                print("No questions found with provided keywords: {keywords}".format(keywords = keywords))
        elif (action == "3" or action == "exit"): # exit the program
            print("exiting...")
            break

    return

if __name__ == "__main__":
    main()