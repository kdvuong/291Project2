class TermParser():
    def __init__(self):
        self.terms = []

    def addTerms(self, data):
        data = data.translate(str.maketrans('', '', string.punctuation)).split(' ')
        seen = {}
        for word in data:
            word = word.lower()
            if len(word) >= 3:
                if word not in seen:
                    seen[word] = 1
                    self.terms.append(word)
    
    def getTerms(self):
        return self.terms

    def clear(self):
        self.terms.clear()