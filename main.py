import argparse
from config.mongoConfig import messages, records
from config.openaiConfig import client
import random
import threading
from typing import List
from models.tools import tools
from config.pineconeConfig import index
import json
import time
import sys
import itertools

class AiReceptionist:
    def __init__(self):
        self.prompt: str = """
        You are a emergency services helper who will ask the user if they have a message to send or is there an emergency. 
        If the user replies that they have a message to send. Ask the user for what message do they need to send. Once they say the message we need to call the store_user_message function and let the user know their message has been sent to Dr. Adrin.
        If they have an emergency ask them what is the emergency that they are facing. Be helpful and empathetic. If the user has mentioned an emergency, the model will call the function fetch_emergency_action to provide immediate actions that should be taken during an emergency until professional medical help arrives. Do not provide any steps by your own, just calling the function would provide them the steps. Keep them engaged and tell them help is on the way.
        If the role assistant is called, provide the users with the raw content in assistant for steps to do now. If the role assistant has not provided the ways to help the user yet, tell them that  "Please hold just a sec"
        If the user gives a location or locality or place, call the fetch_user_location function to provide an estimated time of arrival for assistance and tell help is on the way. If the user says that the time you provided will be too late, tell them : "Don't worry, please follow these steps, Dr. Adrin will be with you shortly".
        If at any point the user says something unrelated, say "I don't understand that and repeat the question/statement".
        """
        self.tools: List = tools  # dict of tools
        self.messages: List = list()  # messages buffer
        self.model = "gpt-4o"
        self.messages.append({"role": "system", "content": self.prompt})
    
    def make_openai_call(self):
        response = client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools,
            tool_choice="auto",
        )
        return response
    
    def get_response(self, user_message):
        self.messages.append({"role": "user", "content": user_message})
        # make the completion call: this would have a tool response as well
        response = self.make_openai_call()
        # make a completion call to handle the tool call and reply with a reponse
        response_message = response.choices[0].message
        self.messages.append(response.choices[0].to_dict()['message'])
        return self.handle_response(response)
    
    def handle_response(self, response):
        # print("RESPONSE", response)
        tool_calls = response.choices[0].message.tool_calls
        if tool_calls:
            return self.handle_tool_call(tool_calls)
        assistant_response = response.choices[0].message.content
        return assistant_response
        
    def handle_tool_call(self, tool_calls):
        for tool in tool_calls:
            if tool.function.name == "fetch_user_location":
                location = json.loads(tool.function.arguments)['location']
                eta = self.get_eta_on_location(location)
                response = f"Please hold on for a while, dr adrin will be there in {eta} minutes"
                # print(respo)
                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool.id,
                        "name": tool.function.name,
                        "content": response,
                    }
                )

            if tool.function.name == "fetch_emergency_action":
                # Fetch emergency action asynchronously
                # self.FETCHING = True
                thread = threading.Thread(target=self.fetch_emergency_action, args=(json.loads(tool.function.arguments)['emergency'], tool))
                thread.start()
                response = {
                    "role": "tool",
                    "tool_call_id": tool.id,
                    "name": tool.function.name,
                    "content": f"Success 400. Tell the user that 'I am checking what you should do immediately, meanwhile, can you tell me which area are you located right now.' Do not provide any steps by your own, just calling the function would provide them the steps.",
                }
                self.messages.append(response)

            if tool.function.name == "store_user_message":
                # store the message in the database
                tool_query_string = json.loads(tool.function.arguments)['message']
                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool.id,
                        "name": tool.function.name,
                        "content": f"Success 400. Message: {tool_query_string} has been sent to Dr. Adrin",
                    }
                )
        response = self.make_openai_call()
        return response.choices[0].message.content
    
    def get_eta_on_location(self, location: str):
        # print("LOCATION FUNCTION CALLED")
        return random.randint(5, 20)
    
    def fetch_emergency_action(self, emergency: str, tool):
        # delay for 15 secs
        time.sleep(15)
        # Suppose response is fetched from the vector database
        # self.FETCHING = False
        search_string = client.embeddings.create(
        input = emergency,
        model = "text-embedding-ada-002"
        )

        document = index.query(
            vector=search_string.data[0].embedding,
            top_k=1
        )
        
        for match in document['matches']:
            match_id = match['id']
            match_score = match['score']

        response = records.find_one({'emergency_type': match_id})["action"]
        self.messages.append({
            "role": "assistant",
            # "tool_call_id": tool.id,
            # "name": tool.function.name,
            "content": response
        })        
        print("\nSteps to follow : ", response)

def generating_animation():
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    while getattr(threading.current_thread(), "do_run", True):
        sys.stdout.write(f"\rGenerating... {next(spinner)}")
        sys.stdout.flush()
        time.sleep(0.1)

def main():
    parser = argparse.ArgumentParser(description="AI Receptionist CLI")
    parser.add_argument("--start", action="store_true", help="Start the chat with the AI receptionist")
    args = parser.parse_args()

    if args.start:
        assistant = AiReceptionist()
        print("AI Receptionist: Hi I am an Asclepius, your ai-receptionist. How can I help you today? Do you have an emergency or a message to send?")
        while True:
            user_message = input("\nYou: ")
            if user_message.lower() in ["exit", "quit", "bye", "goodbye"]:
                print("AI Receptionist: Goodbye!")
                break
            
            # Start the generating animation in a separate thread
            animation_thread = threading.Thread(target=generating_animation)
            animation_thread.daemon = True
            animation_thread.start()
            
            # Get the response
            response = assistant.get_response(user_message)
            
            # Stop the animation
            animation_thread.do_run = False
            animation_thread.join()
            
            # Clear the animation line and print the response
            sys.stdout.write('\r' + ' ' * 20 + '\r')
            print(f"\nAI Receptionist: {response}")

if __name__ == "__main__":
    main()