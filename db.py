import pymongo

# Replace with your MongoDB connection string
#connection_string = "mongodb+srv://admin:admin123@cluster0.147cmvg.mongodb.net/?retryWrites=true&w=majority"
connection_string = "mongodb://localhost:27017"

class Db:
    def __init__(self, connection_string):
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client["ChatBot"]
        self.users = self.db["users"]
        self.collection = self.db["abcd2"]
        self.cat = "hi"
        self.cache = {}

    def check_if_exist(self, query):
        document = self.collection.find_one(query)
        return document is not None

    def insert_entry(self, document):
        if not self.check_if_exist(document):
            self.collection.insert_one(document)
            self.cache[document["_id"]] = document

    def delete_entry(self, query):
        self.collection.delete_one(query)
        for document in self.cache.values():
            if document["_id"] == query["_id"]:
                del self.cache[document["_id"]]

    def update_entry(self, query, update):
        self.collection.update_one(query, update)
        for document in self.cache.values():
            if document["_id"] == query["_id"]:
                document.update(update)

    def list_all_entries(self):
        for document in self.users.find(): #collection.find():
            print(document)

    def close_connection(self):
        self.client.close()

""" 
# Create a document to insert
document = {
    "name": "John Doe",
    "age": 37,
    "city": "New York"
}

x = Db(connection_string)
#print(x.check_if_exist(document))
#x.insert_entry(document)
print("inserted successfully")
print("*"*5)
#x.list_all_entries()
print(x.cat)
""" 

db = Db(connection_string)
#db.users.insert_one({"fname":"abcd", "email":"a@b.co".lower(),"pnum":1234567890, "pass":"a"})
#db.list_all_entries()