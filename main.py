import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Read Telegram bot token from environment variable
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]

# Basic start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to AdvanceOptionsGptBot!\nUse /ask followed by your question.")

# Echo handler for /ask
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = " ".join(context.args)
    if not user_input:
        await update.message.reply_text("Please provide a question after /ask.")
    else:
        await update.message.reply_text(f"🤖 Your question was: {user_input}\n(Answer will be AI-integrated soon)")

# Main function to run bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    app.run_polling()

if __name__ == "__main__":
    main()
