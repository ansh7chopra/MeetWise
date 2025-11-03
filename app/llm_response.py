import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"  

def query_llm(prompt: str) -> str:
    if not GROQ_API_KEY:
        raise ValueError("Missing GROQ_API_KEY. Set it in your .env file.")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful AI meeting assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 1024
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=body)

    if response.status_code != 200:
        raise RuntimeError(f"Groq API Error {response.status_code}: {response.text}")

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
