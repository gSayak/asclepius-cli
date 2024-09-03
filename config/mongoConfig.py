from pymongo import MongoClient
from config.config import MONGO_DB_URI, MONGO_DB_NAME

client_db = MongoClient(MONGO_DB_URI)
db = client_db.get_database(MONGO_DB_NAME)
records = db.reception 
messages = db.messages