import requests

API_KEY = "AIzaSyBaEkH22TT2pmiJe-KHcAxuaXpOeKGh2Bc"

url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
payload = {
    "contents": [{
        "parts":[{"text":"Say hello"}]
    }]
}

r = requests.post(url, json=payload)
print(r.status_code)
print(r.json())