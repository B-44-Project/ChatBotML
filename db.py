import pymongo

#connection_string = "mongodb+srv://admin:admin123@cluster0.147cmvg.mongodb.net/?retryWrites=true&w=majority"
connection_string = "mongodb://localhost:27017"

class Db:
    def __init__(self, connection_string):
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client["ChatBot"]
        self.users = self.db["users"]
        self.chats = self.db["conversations"]
        self.collection = self.db["abcd2"]
        self.cache = {}

    def close_connection(self):
        self.client.close()

db = Db(connection_string)
