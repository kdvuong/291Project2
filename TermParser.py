import string

class TermParser():
    def __init__(self):
        self.seen = {}
        self.terms = []

    def addTerms(self, data):
        data = data.translate(str.maketrans('', '', string.punctuation)).split(' ')
        for word in data:
            word = word.lower()
            if len(word) >= 3:
                if word not in self.seen:
                    self.seen[word] = 1
                    self.terms.append(word)
    
    def getTerms(self):
        return self.terms

    def clear(self):
        self.terms.clear()
        self.seen = {}