from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

class database:
    def __init__(self):
        self.uri = os.environ.get("MONGO_URI")
        self.client = MongoClient(self.uri)#, server_api=ServerApi('1'))
        self.db = self.client["mydatabase"]
        self.collection = self.db["mycollection"]
        self.ping()

    def ping(self):
        self.client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
