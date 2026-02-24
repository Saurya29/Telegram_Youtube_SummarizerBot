import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

def generate(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [{
            "role": "user",
            "parts": [
                {"text": prompt}
            ]
        }]
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    # If Gemini blocks or fails
    if "candidates" not in data:
        print("Gemini Raw Response:", data)   # debug
        return "⚠️ Gemini could not generate response. Please try again."

    return data["candidates"][0]["content"]["parts"][0]["text"]