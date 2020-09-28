# encoding: utf-8

# Telegram API framework core imports
from telegram.ext import Dispatcher, CallbackContext
from telegram import Update, InlineKeyboardMarkup
# Helper methods import
from utils.logger import get_logger
from utils.helpers import *
# Telegram API framework handlers imports
from telegram.ext import CommandHandler, CallbackQueryHandler

# Init logger
logger = get_logger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""

    dispatcher.add_handler(CommandHandler('menu', menu))
    dispatcher.add_handler(CallbackQueryHandler(callback))


def menu(update: Update, context: CallbackContext) -> None:
    # Stupid state machine realization
    if context.bot_data['notify_dict'].get(update.effective_user.id,None) == True:
        pass
    button_list = [
        InlineKeyboardButton("col1", callback_data=1),
        InlineKeyboardButton("col2", callback_data=2),
        InlineKeyboardButton("row 2", callback_data=3)
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    context.bot.send_message(update.effective_message.chat_id, 'Меню', reply_markup=reply_markup)


def callback(update: Update, context: CallbackContext):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text="Selected option: {}".format(query.data))
