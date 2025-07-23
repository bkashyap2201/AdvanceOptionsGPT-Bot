import os
import logging
from openai import OpenAI
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Read environment variables
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")  # Default model

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with bot instructions"""
    welcome_msg = (
        "🤖 Welcome to AdvanceOptionsGptBot!\n\n"
        "How to use:\n"
        "/ask <your question> - Get AI-powered answers\n"
        "/model - Show current AI model\n"
        "Example: /ask Explain quantum computing in simple terms"
    )
    await update.message.reply_text(welcome_msg)

async def model_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current AI model information"""
    await update.message.reply_text(f"🔧 Current AI model: {OPENAI_MODEL}")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process user questions with AI"""
    user_input = " ".join(context.args).strip()
    
    # Validate input
    if not user_input:
        await update.message.reply_text("ℹ️ Please provide a question after /ask")
        return

    try:
        # Send processing indicator
        processing_msg = await update.message.reply_text("⏳ Processing your question...")
        
        # Get AI response
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": user_input}],
            max_tokens=1500,
            temperature=0.7
        )
        
        # Extract and format response
        ai_response = response.choices[0].message.content.strip()
        
        # Delete processing message
        await processing_msg.delete()
        
        # Handle long responses
        if len(ai_response) <= constants.MAX_MESSAGE_LENGTH:
            await update.message.reply_text(f"🤖 {ai_response}")
        else:
            # Split long responses into multiple messages
            parts = [ai_response[i:i+constants.MAX_MESSAGE_LENGTH] 
                     for i in range(0, len(ai_response), constants.MAX_MESSAGE_LENGTH)]
            for part in parts:
                await update.message.reply_text(part)
                
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        error_msg = (
            "⚠️ Sorry, I encountered an error processing your request. "
            "Please try again later or rephrase your question."
        )
        await update.message.reply_text(error_msg)

def main():
    """Start the bot"""
    # Validate environment variables
    required_vars = ["TELEGRAM_TOKEN", "OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.critical(f"Missing environment variables: {', '.join(missing_vars)}")
        raise RuntimeError("Missing required environment variables")
    
    # Build and configure application
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CommandHandler("model", model_info))
    
    # Start polling
    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
