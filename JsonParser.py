import json

class JsonParser:        
    def getData(self, fileName):
        with open(fileName) as json_file:
            data = json.load(json_file)
            return data

# j = JsonParser()
# data = j.getData('Votes.json')
# print(data)

