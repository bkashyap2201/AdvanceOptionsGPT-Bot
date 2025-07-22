import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai
import requests

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Read environment variables (tokens)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Set OpenAI key
openai.api_key = OPENAI_API_KEY

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("👋 Welcome to AdvanceOptionsGptBot!\n\nType /ask followed by your question or wait for breakout alerts.")

# /ask command
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("❗Please provide a question. Example: `/ask What is a breakout in options trading?`")
        return
    
    user_question = " ".join(context.args)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert options trading assistant."},
                {"role": "user", "content": user_question}
            ]
        )
        reply = response.choices[0].message.content.strip()
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

# Set up application and handlers
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    
    # Add other command handlers for breakout alerts later
    app.run_polling()

if __name__ == '__main__':
    main()
