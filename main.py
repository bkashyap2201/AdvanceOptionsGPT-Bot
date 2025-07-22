import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Example /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome to Advance Options GPT Bot!")

# Example /ask command
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("Please enter a query after /ask.")
        return
    # Dummy response for now
    await update.message.reply_text(f"Received your query: {query}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))

    app.run_polling()
