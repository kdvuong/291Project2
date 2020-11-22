import json

# Class to handle parsing the json files
class JsonParser:
    # Function to get the data from the json files
    def getData(self, fileName):
        with open(fileName) as json_file:
            data = json.load(json_file)
            return data
