from html.parser import HTMLParser
from TermParser import TermParser
import string

termParser = TermParser()

class TextParser(HTMLParser):
    def handle_data(self, data):
        formatted = data.translate(str.maketrans('', '', string.punctuation))
        termParser.addTerms(formatted)
        
textParser = TextParser()

class Parser():
    def parse(self, s):
        termParser.clear()
        textParser.feed(s)
        return termParser.getTerms()

    def getParsed(self):
        return termParser.getTerms()
