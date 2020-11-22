import pymongo
import sys
from pymongo import MongoClient
from Parser import Parser


# Function to connect to MongoDb server based on cloud/port number
def getDb():
    client = None
    db = None
    dbName = "291db"

    if (len(sys.argv) == 2):
        if (sys.argv[1].lower() == "cloud"):
            client = MongoClient("mongodb+srv://khang:Khang99!@cluster0.27zhi.mongodb.net/{name}?retryWrites=true&w=majority".format(name = dbName))
            print("Connected to mongodb cluster")
        else:
            try:
                port = int(sys.argv[1])
                client = MongoClient("localhost", port)
                print("Connected to local mongodb server on port: {port}".format(port = port))
            except:
                raise Exception("Invalid port input.")
    else:
        raise Exception("Try again with: python3 {program} 'cloud | port_number'".format(program = sys.argv[0]))

    if (client != None):
        db = client[dbName]

    return db
