from pinecone import Pinecone
from config.config import PINECONE_DB_KEY

pc = Pinecone(api_key=PINECONE_DB_KEY)
index = pc.Index("emergency-db") 