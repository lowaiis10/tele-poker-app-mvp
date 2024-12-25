import os, logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from bot import *

load_dotenv()

# Replace with your actual bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")


# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,  # Ensure logs are displayed at INFO level or higher
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler("bot_interactions.log")  # Log to file
    ]
)
logger = logging.getLogger(__name__)

# Middleware to log all incoming updates
async def log_all_updates(update, context: ContextTypes.DEFAULT_TYPE):
    """Log every incoming update globally."""
    if update.effective_message:
        logger.info(f"Message: {update.effective_message.text}")
    if update.effective_user:
        logger.info(f"User: {update.effective_user.username or update.effective_user.id}")
    if update.effective_chat:
        logger.info(f"Chat ID: {update.effective_chat.id}")

    # Proceed with processing the update
    await context.application.process_update(update)

# Error handler to log exceptions
async def log_errors(update, context: ContextTypes.DEFAULT_TYPE):
    """Log all errors globally."""
    logger.error(f"Update {update} caused error {context.error} \n", exc_info=True)

def main():
    # Step 1: Set up the database
    create_tables()  # Ensures all new database tables are created.

    # Step 2: Initialize the bot using Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Step 3: Add command handlers
    # /start - Greets the user
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # /create_game - Creates a new game with specified blinds
    #application.add_handler(CommandHandler("create_game", create_game))

    # /join_game - Allows a player to join an existing game with specified blinds and cash-in amount
    #application.add_handler(CommandHandler("join_game", join_game))

    # /start_game - Starts the game once enough players have joined
    #application.add_handler(CommandHandler("start_game", start_game))

    # Step 4: Start the bot
    print("🤖 Bot is running! Use /start to begin.")
    application.run_polling()

if __name__ == "__main__":
    main()
