tools = [
    {
        "type": "function",
        "function": {
            "name": "store_user_message",
            "description": "Capture and store the message provided by the user for later retrieval or action.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message content provided by the user, e.g., 'Hello Doctor, will you be available tomorrow?'"
                    }
                },
                "required": ["message"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_emergency_action",
            "description": "Provide immediate actions that should be taken during an emergency until professional medical help arrives.",
            "parameters": {
                "type": "object",
                "properties": {
                    "emergency": {
                        "type": "string",
                        "description": "A brief description of the current emergency situation, e.g., 'patient is not breathing', 'severe bleeding', 'choking incident'."
                    }
                },
                "required": ["emergency"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_user_location",
            "description": "Obtain the user's location to provide an estimated time of arrival for assistance be it nearby location or the exact location provided. Only call this function when there is an explicit location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The specific location where the incident occurred, e.g., 'park in the Bay Area, San Francisco' or 'Kolkata, India'."
                    }
                },
                "required": ["location"],
                "additionalProperties": False
            }
        }
    }
]