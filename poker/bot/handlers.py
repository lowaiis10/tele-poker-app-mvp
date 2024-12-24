from telegram import Update
from telegram.ext import ContextTypes
from bot.game_logic import create_new_game, add_player_to_game, start_poker_game

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Poker Bot! Use /create_game to start a game.")

# /create_game command
async def create_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    game_id = create_new_game(chat_id)
    await update.message.reply_text(f"🃏 A new poker game has been created! Game ID: {game_id}")

# /join_game command
async def join_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    username = update.effective_user.username

    success = add_player_to_game(chat_id, user_id, username)
    if success:
        await update.message.reply_text(f"✅ {username} has joined the game!")
    else:
        await update.message.reply_text("❌ Failed to join the game. Is there an active game?")

# /start_game command
async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    success = start_poker_game(chat_id)
    if success:
        await update.message.reply_text("🔥 The game has started! Good luck!")
    else:
        await update.message.reply_text("❌ Failed to start the game. Ensure enough players have joined.")
