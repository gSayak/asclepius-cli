from pymongo import MongoClient
from config.config import MONGO_DB_URI

client_db = MongoClient(MONGO_DB_URI)
db = client_db.get_database('asclepius')
records = db.reception 
messages = db.messages