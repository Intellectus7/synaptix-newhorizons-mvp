import os
from google import genai
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# API keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Clients
gemini_client = genai.Client(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

def explain_error(err):
    msg = str(err)

    if "RESOURCE_EXHAUSTED" in msg:
        return "Gemini quota exceeded."

    if "403" in msg:
        return "Groq access denied."

    if "401" in msg:
        return "Invalid API key."

    if "429" in msg:
        return "Rate limited."

    return msg[:200]

def answer_query(question):
    gemini_error = None
    groq_error = None

    # 1. Try Gemini first
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question
        )
        return response.text

    except Exception as error:
        gemini_error = str(error)

    # 2. Fallback to Groq
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": question}
            ]
        )

        return response.choices[0].message.content

    except Exception as error:
        groq_error = str(error)

    # 3. Both failed
    return (
        "Sorry, I couldn't generate a response right now.\n\n"
        "Details:\n"
        f"- Gemini failed: {explain_error(gemini_error)}\n"
        f"- Groq failed: {explain_error(groq_error)}\n\n"
        "This usually happens because of an invalid API key, a network "
        "connectivity issue, rate limiting, temporary provider downtime, "
        "or a model/service configuration problem."
    )
