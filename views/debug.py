# encoding: utf-8

# Telegram API framework core imports
from telegram.ext import Dispatcher, CallbackContext, CommandHandler
from telegram import Update
# Helper methods import
from utils.logger import get_logger

# Init logger
logger = get_logger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('info', info))


def info(update: Update, context: CallbackContext) -> None:
    message = f'bot info\n' \
              f'first_name: {context.bot.first_name}\n' \
              f'name: {context.bot.name}\n' \
              f'username: {context.bot.username}\n' \
              f'id: {context.bot.id}\n\n' \
              f'You info.\n' \
              f'first_name: {update.effective_user.first_name}\n' \
              f'last_name: {update.effective_user.last_name}\n' \
              f'id: {update.effective_user.id}\n\n' \
              f'Chat info.\n' \
              f'first_name: {update.effective_chat.first_name}\n' \
              f'last_name: {update.effective_chat.last_name}\n' \
              f'id: {update.effective_chat.id}\n' \
              f'type: {update.effective_chat.type}\n'
    context.bot.send_message(update.effective_chat.id,message)