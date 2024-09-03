import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPEN_AI_KEY")
PINECONE_DB_KEY = os.getenv("PINECONE_DB")
MONGO_DB_URI = os.getenv("MONGO_DB_URI")

