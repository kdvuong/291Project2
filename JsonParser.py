import json

class JsonParser:
    def __init__(self, fileName):
        self.fileName = fileName
    
    def getData(self):
        with open(self.fileName) as json_file:
            data = json.load(json_file)
            return data

# j = JsonParser('Posts.json')
# data = j.getData()
# print(data)

