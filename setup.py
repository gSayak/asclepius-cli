from models.instructions import emergency_instructions
from config.openaiConfig import client
from config.pineconeConfig import index
from config.mongoConfig import records

class Setup:
    def __init__(self):
        self.emergency_instructions = emergency_instructions
        self.data_to_upsert = list()
        self.records_to_insert = list()

    def create_embedding(self, text):
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        embedding = response.data[0].embedding
        return embedding

    def setup_pinecone(self):
        for title, instruction in self.emergency_instructions.items():
            embedding = self.create_embedding(f"It seems to be a case of {title}. {instruction}")
            self.data_to_upsert.append((title, embedding))
        index.upsert(self.data_to_upsert)
        print("Pinecone setup complete")

    def setup_mongo(self):
        self.records_to_insert = [{"emergency_type": key, "action": value} for key, value in emergency_instructions.items()]
        records.insert_many(self.records_to_insert)
        print("Mongo setup complete")

    def setup(self):
        self.setup_pinecone()
        self.setup_mongo()


if __name__ == "__main__":
    setup = Setup()
    setup.setup()
