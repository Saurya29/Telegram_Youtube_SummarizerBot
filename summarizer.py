from groq_client import generate

def summarize(text, language="English"):
    prompt = f"""
You are a professional research assistant.

Summarize the YouTube transcript below in {language}.

Follow this STRICT format:

🎥 Video Title:
(one line)

📌 5 Key Points:
- Point 1
- Point 2
- Point 3
- Point 4
- Point 5

⏱ Important Timestamps:
- Timestamp - Topic
- Timestamp - Topic
(If timestamps are not present, write: Not available)

🧠 Core Takeaway:
(one paragraph)

Rules:
- Be concise
- Do NOT hallucinate
- Base everything only on transcript

Transcript:
{text}
"""
    return generate(prompt)