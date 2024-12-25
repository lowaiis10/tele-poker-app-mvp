import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.front_end import *

logger = logging.getLogger(__name__)

POKER_RULES = """
📜 *Poker Rules*

*Game Type*: Texas Hold'em No\-Limit Poker

*Objective*: Win chips by having the best 5\-card hand or by getting all opponents to fold\.

*Card Dealing*:
• Each player gets *2 Hole Cards* \(face down\)\.
• *Community Cards* are dealt in 3 stages:
  • *Flop*: 3 cards are dealt face up\.
  • *Turn*: 1 card is dealt face up\.
  • *River*: 1 final card is dealt face up\.

*Betting Rounds*:
• *Pre\-Flop*: Players act after receiving Hole Cards\.
• *Post\-Flop*: Betting occurs after the Flop is revealed\.
• *Post\-Turn*: Betting occurs after the Turn card is revealed\.
• *Post\-River*: Final betting occurs after the River card is revealed\.

*Actions*:
• *Check*: Pass without betting if no bet has been made\.
• *Call*: Match the current bet\.
• *Raise*: Increase the current bet\.
• *Fold*: Discard your hand and exit the round\.

*Winning*:
• Best hand wins the pot\.
• If all opponents fold, the remaining player wins the pot\.

*Time Limit*:
• Players have *2 minutes* to make a move or they fold automatically\.

*Etiquette*:
• Play fair, and no external discussions about ongoing hands\.

Enjoy playing\! 🎉
"""

async def handle_view_rules(query):
    """Handles the 'View Rules' button click."""
    logger.info("User selected 'View Rules'.")
    keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=POKER_RULES,
        reply_markup=reply_markup,
        parse_mode="MarkdownV2"
    )


async def handle_support_server(query):
    """Handles the 'Support Server' button click."""
    logger.info("User selected 'Support Server'.")
    keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="🌐 Support Server: [www.deeznutz.xyz]\nIf you need any help, join our community!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def exit_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Exit the bot interaction with a thank-you message.
    """
    logger.info(f"User {update.effective_user.username} exited the game.")

    # Send an exit message
    await update.callback_query.edit_message_text(
        "Thanks for playing! 🎉 Feel free to return anytime by clicking /start."
    )