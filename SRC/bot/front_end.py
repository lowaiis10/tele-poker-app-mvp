import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.game_logic import create_new_game, add_player_to_game, start_poker_game

# Intiaite logger for user interactions
logger = logging.getLogger(__name__)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Start command handler that shows the main menu.
    Handles both direct messages and callback queries.
    """
    logger.info(f"User {update.effective_user.username} issued /start command.")

    keyboard = [
  
        [InlineKeyboardButton("Join Game", callback_data="join_game")],
        [InlineKeyboardButton("View Rules", callback_data="view_rules")],
        [InlineKeyboardButton("Support Server", callback_data="support_server")],
        [InlineKeyboardButton("Exit", callback_data="exit_game")],  # Add Exit button
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:  # Check if this is a direct message
        await update.message.reply_text(
            "Welcome to the $SOL Poker! Select an option below:",
            reply_markup=reply_markup,
        )
    elif update.callback_query:  # Handle callback query (button press)
        query = update.callback_query
        await query.edit_message_text(
            text="Welcome to the $SOL Poker! Select an option below:",
            reply_markup=reply_markup,
        )


# creates a menu to select blinds
async def select_blinds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Displays a menu for selecting blinds.
    """
    query = update.callback_query  # Access the callback query from the button click
    await query.answer()  # Acknowledge the button press

    keyboard = [
        [InlineKeyboardButton("🐟 Blind: 0.01 $SOL", callback_data='point_zero_one')],
        [InlineKeyboardButton("🐬 Blind: 0.1 $SOL", callback_data='point_one')],
        [InlineKeyboardButton("🐋 Blind: 1 $SOL", callback_data='one')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="Please select your blinds:",
        reply_markup=reply_markup
    )


################################# 

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
