from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb://192.168.0.101:27017/"

client = MongoClient(uri, server_api=ServerApi("1"))
database = client["materialDB"]
