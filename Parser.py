from html.parser import HTMLParser
from TermParser import TermParser

termParser = TermParser()

class TextParser(HTMLParser):
    def handle_data(self, data):
        termParser.addTerms(data)
        
textParser = TextParser()


class Parser():
    def __init__(self):
        self.parsed = []

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

    def parseTags(self, tags):
        tags = tags.replace("<", "")
        tags = tags.split(">")
        tags.pop()
        self.parsed = tags
        return self.parsed.copy()

    def getParsed(self):
        return self.parsed.copy()
