import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq() 

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
