# Asclepius: AI Emergency Services Assistant

Asclepius is an AI-powered emergency services assistant that helps users send messages or get immediate assistance during emergencies.

## Features

- Emergency response guidance
- Message relay to Dr. Adrin
- Estimated time of arrival for assistance
- Interactive CLI interface with loading animation

## Prerequisites

- Python 3.7+
- MongoDB
- Pinecone account
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/gSayak/asclepius-cli.git
   cd asclepius
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with the following:
   ```
   OPEN_AI_KEY=your_openai_api_key
   PINECONE_DB=your_pinecone_api_key
   MONGO_DB_URI=your_mongodb_uri
   ```

## Usage

Run the AI receptionist:

```
python main.py --start
```

Interact with the AI by responding to its prompts. You can:
- Send a message to Dr. Adrin
- Describe an emergency situation
- Provide your location for assistance
- Exit the conversation

## Project Structure

- `main.py`: Contains the `AiReceptionist` class and CLI interface
- `config/`: Configuration files for OpenAI, Pinecone, and MongoDB
- `models/`: Defines the tools used by the AI

## Key Components

### AiReceptionist Class

The main class that handles user interactions, API calls, and response processing.


### Configuration

The project uses environment variables for configuration:


### Database Interactions

- MongoDB for storing messages and records
- Pinecone for vector similarity search of emergency actions

### OpenAI Integration

Uses the OpenAI API for natural language processing and response generation.


## License

This project is licensed under the [MIT License](LICENSE).
