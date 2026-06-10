import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://portkey.ai",
    default_headers={
        "x-portkey-api-key": os.environ.get("PORTKEY_API_KEY"), # Get from portkey
        "x-portkey-provider": "groq"
    }
) 

def answer_query(question):
    try:
        chat_completions = client.chat.completions.create(
            messages = [{
                'role': 'user',
                'content': question
    
            }],
            model = "llama-3.3-70b-versatile",
        )
        return chat_completions.choices[0].message.content
    except Exception as error:
        return f"GROQ ERROR: {str(error)}"
