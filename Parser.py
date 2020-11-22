from html.parser import HTMLParser
from TermParser import TermParser

termParser = TermParser()

# Class to handle text parsing
class TextParser(HTMLParser):
    # function to parse data as term
    def handle_data(self, data):
        termParser.addTerms(data)
        
textParser = TextParser()

# Class to handle parsing
class Parser():
    def __init__(self):
        self.parsed = []

    # function to handle parsing title and body
    def parseTitleAndBody(self, arg = {
        "title": "",
        "body": ""
    }):
        if (arg["title"] == "" and arg["body"] == ""):
            return
        
        termParser.clear()

        if (arg["title"] != ""):
            termParser.addTerms(arg["title"])
        
        if (arg["body"] != ""):
            textParser.feed(arg["body"])

        self.parsed = termParser.getTerms()
        return self.parsed.copy()

    # function to handle parsing tags
    def parseTags(self, tags):
        tags = tags.replace("<", "")
        tags = tags.split(">")
        tags.pop()
        self.parsed = tags
        return self.parsed.copy()

    # function to return the parsing terms
    def getParsed(self):
        return self.parsed.copy()
