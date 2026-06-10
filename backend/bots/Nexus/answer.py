import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
my_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(
    api_key=my_api_key
)

def answer_query(question):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question
        )

        return response.text

    except Exception as error:
        return f"GEMINI ERROR: {str(error)}"
