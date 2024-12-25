import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.front_end import *
from bot.handlers import *



# Configure logging for middleware
logger = logging.getLogger(__name__)

# Routes user interaction to button command
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "back_to_menu":
        await start(update, context)
    elif query.data == "join_game":
        await select_blinds(update, context)
    elif query.data == "view_rules":
        await handle_view_rules(query)
    elif query.data == "support_server":
        await handle_support_server(query)
    elif query.data == "exit_game":
        await exit_game(update, context)  # Call the exit_game function
    else:
        await query.edit_message_text("❌ Invalid selection. Please try again.")




    

