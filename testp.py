from pymongo import MongoClient
client = MongoClient()
from bson import ObjectId
db = client['todo']
collection = db['user']
collection.insert_one({'user': 'yu', 'password': 'yu123'})
