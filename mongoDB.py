from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os



class database:
    def __init__(self):
        self.status = os.environ.get("APP_STATUS", "LOCAL")

        if self.status=="LOCAL":
            from keys import mongo_uri
            self.uri = mongo_uri
        elif self.status=="DEPLOY":
            self.uri = os.environ.get("MONGO_URI")

        #forest:
        # self.uri = os.environ.get("MONGO_URI")
        ## self.uri = "mongodb+srv://fssong7:GE0SsNARhMKigDzv@cluster0.wqhp1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.db = self.client["mydatabase"]
        self.collection = self.db["mycollection"]
        #self.ping()

    def ping(self):
        self.client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
