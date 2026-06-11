import os
import random  # FIX: Added missing import
from dotenv import load_dotenv
from google import genai  # Ensure 'google-genai' is in requirements.txt
from groq import Groq
from openai import OpenAI

load_dotenv()

# =========================
# Environment Variables
# =========================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # FIX: Normalized naming

required_keys = {
    "GEMINI_API_KEY": GEMINI_API_KEY,
    "GROQ_API_KEY": GROQ_API_KEY,
    "OPEN_ROUTER_API_KEY": OPEN_ROUTER_API_KEY,
    "GITHUB_TOKEN": GITHUB_TOKEN
}

for name, value in required_keys.items():
    if not value:
        raise ValueError(f"Missing environment variable: {name}")

# =========================
# Clients
# =========================

gemini_client = genai.Client(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

open_router_client = OpenAI(
    api_key=OPEN_ROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

github_client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=GITHUB_TOKEN
)

# =========================
# Models
# =========================

GEMINI_MODEL = "gemini-2.5-flash"
GROQ_MODEL = "llama-3.3-70b-versatile"
OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct:free"

LOW_TIER_MODELS = [
    "meta-llama-3.1-8b-instruct",
    "gpt-4o-mini",
    "mistral-large-2407", 
    "cohere-command-r"
]

HIGH_TIER_MODELS = [
    "meta-llama-3.3-70b-instruct",
    "gpt-4o"
]

# =========================
# Helpers
# =========================

def explain_error(err):
    if not err:
        return "No error recorded"
    msg = str(err)
    if "RESOURCE_EXHAUSTED" in msg:
        return "Gemini quota exceeded."
    if "401" in msg:
        return "Invalid API key."
    if "403" in msg:
        return "Access denied."
    if "429" in msg:
        return "Rate limited."
    return msg[:200]

def generate_ai_response(prompt, critical_task=False):
    """
    Shuffles model selection to distribute requests across separate quotas.
    If all internal models fail, it raises an exception to trigger the main loop fallback.
    """
    model_pool = HIGH_TIER_MODELS[:] if critical_task else LOW_TIER_MODELS[:]
    random.shuffle(model_pool)

    for model in model_pool:
        try:
            # FIX: Changed from 'client' to 'github_client'
            response = github_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
                temperature=0.3,
                max_tokens=300
            )
            # FIX: Correct direct property retrieval for standard completions
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"GitHub Model {model} failed: {e}")
            continue
                
    # FIX: Raise an error if exhausted so the main Router moves to OpenRouter
    raise RuntimeError("All pooled GitHub models exhausted or rate limited.")

# =========================
# Providers
# =========================

def answer_gemini(question):
    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=question,
    )
    return response.text

def answer_groq(question):
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content

def answer_openrouter(question):
    response = open_router_client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content

# =========================
# Main Router
# =========================

def answer_query(question):
    # Order: GitHub Pool (Cleanest) -> OpenRouter -> Gemini -> Groq (Most Blocked)
    providers = [
        ("Github", generate_ai_response),
        ("OpenRouter", answer_openrouter),
        ("Gemini", answer_gemini),
        ("Groq", answer_groq),
    ]

    errors = {}

    for provider_name, provider_func in providers:
        try:
            answer = provider_func(question)
            if answer: # Ensure we didn't get an empty response
                return f"[{provider_name}]\n{answer}"
        except Exception as error:
            errors[provider_name] = explain_error(error)

    return (
        "Sorry, I couldn't generate a response right now.\n\n"
        "Provider Errors:\n"
        + "\n".join(f"- {name}: {error}" for name, error in errors.items())
    )

if __name__ == "__main__":
    question = input("Ask something: ")
    print(answer_query(question))
