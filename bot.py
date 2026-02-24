import logging
import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes
)

from utils import extract_video_id, get_transcript
from summarizer import summarize
from qa import answer_question

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

user_sessions = {}  



def detect_language(text: str) -> str:
    text = text.lower()
    if "hindi" in text:
        return "Hindi"
    return "English"



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Send me a YouTube link and I will summarize it.\n"
        "Then you can ask questions about the video.\n\n"
        "Examples:\n"
        "- Summarize in Hindi\n"
        "- What did he say about pricing?"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Start bot\n"
        "Send YouTube link - Get summary\n"
        "Ask questions after summary\n"
        "Use: summarize in hindi"
    )



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        chat_id = update.message.chat_id

        if "youtube.com" in text or "youtu.be" in text:

            await update.message.reply_text("Fetching transcript...")

            video_id = extract_video_id(text)
            transcript = get_transcript(video_id)

            # Trim very long transcripts
            transcript = transcript[:12000]
            user_sessions[chat_id] = transcript

            language = detect_language(text)
            summary = summarize(transcript, language)

            await update.message.reply_text(summary)

       
        else:
            if chat_id not in user_sessions:
                await update.message.reply_text(
                    "Please send a YouTube link first."
                )
                return

            language = detect_language(text)
            answer = answer_question(user_sessions[chat_id], text, language)

            await update.message.reply_text(answer)

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text(
            "⚠️ Unable to process request. Try another video."
        )



app = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .connect_timeout(20)
    .read_timeout(20)
    .build()
)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

print("🤖 Bot started...")
app.run_polling()