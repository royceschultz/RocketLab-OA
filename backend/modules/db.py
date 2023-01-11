from pymongo import MongoClient
import os

def connect_mongo_client():
    return MongoClient(
        host=os.environ['MONGO_HOST'],
        port=int(os.environ['MONGO_PORT']),
        username=os.environ['MONGO_USERNAME'],
        password=os.environ['MONGO_PASSWORD'],
    )

def connect_mongo():
    return connect_mongo_client()[os.environ['MONGO_DB']]
