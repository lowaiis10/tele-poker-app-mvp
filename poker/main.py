from telegram.ext import Application, CommandHandler
from bot.handlers import create_game, join_game, start_game, start
from bot.database import create_tables

# Replace with your actual bot token
BOT_TOKEN = "7681782621:AAFRVAHcy6S083OaOGXTF0Qr7Lv8HUdq4hk"

def main():
    # Step 1: Set up the database
    create_tables()  # Ensures all new database tables are created.

    # Step 2: Initialize the bot using Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Step 3: Add command handlers
    # /start - Greets the user
    application.add_handler(CommandHandler("start", start))

    # /create_game - Creates a new game with specified blinds
    application.add_handler(CommandHandler("create_game", create_game))

    # /join_game - Allows a player to join an existing game with specified blinds and cash-in amount
    application.add_handler(CommandHandler("join_game", join_game))

    # /start_game - Starts the game once enough players have joined
    application.add_handler(CommandHandler("start_game", start_game))

    # Step 4: Start the bot
    print("🤖 Bot is running! Use /start to begin.")
    application.run_polling()

if __name__ == "__main__":
    main()
