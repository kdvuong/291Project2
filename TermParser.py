import string

# Class to handle Parsing Term
class TermParser():

    # initialization 
    def __init__(self):
        self.seen = {}
        self.terms = []

    # function to add the terms into array
    def addTerms(self, data):
        data = data.translate(str.maketrans('', '', string.punctuation)).split(' ')
        for word in data:
            word = word.lower()
            if len(word) >= 3:
                if word not in self.seen:
                    self.seen[word] = 1
                    self.terms.append(word)
    
    # function to return the terms
    def getTerms(self):
        return self.terms

    # function to clear up the terms
    def clear(self):
        self.terms.clear()
        self.seen = {}