from groq_client import generate

def answer_question(transcript, question, language="English"):
    prompt = f"""
Answer the question using ONLY the transcript below.

If the answer is not present, reply exactly:
"This topic is not covered in the video."

Respond in {language}.

Transcript:
{transcript}

Question:
{question}
"""
    return generate(prompt)