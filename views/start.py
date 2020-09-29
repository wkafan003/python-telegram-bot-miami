# encoding: utf-8

# Telegram API framework core imports
from telegram.ext import Dispatcher, CallbackContext
from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
# Helper methods import
from utils.logger import get_logger
from utils.helpers import *
# Telegram API framework handlers imports
from telegram.ext import CommandHandler, CallbackQueryHandler

# Init logger
logger = get_logger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('start', start))


def start(update: Update, context: CallbackContext) -> None:
    """Process a /start command."""
    context.bot.send_photo(update.effective_message.chat_id, open('assets/mai.png', 'rb'),
                           caption=f"Привет, <code>{update.effective_user.first_name}</code>. Я могу показать тебе "
                                   f"расписание, а также сообщить тебе вечером, какие завтра будут пары. "
                                   f"🇷🇺🇷🇺🇷🇺. Вызовите команду /menu для отображения меню.",
                           parse_mode=ParseMode.HTML)
