# encoding: utf-8

# Telegram API framework core imports
from telegram.ext import Dispatcher, CallbackContext
from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
# Helper methods import
from utils.logger import get_logger
from utils.helpers import *
# Telegram API framework handlers imports
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler

# Init logger
logger = get_logger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.location, location))


def start(update: Update, context: CallbackContext) -> None:
    """Process a /start command."""

    context.bot.send_photo(update.effective_chat.id, open('assets/mai.png', 'rb'),
                           caption=f"Привет, <code>{update.effective_user.first_name}</code>. Я могу показать тебе "
                                   f"расписание, а также сообщить тебе вечером, какие завтра будут пары. "
                                   f"🇷🇺🇷🇺🇷🇺. Вызовите команду /menu для отображения меню.",
                           parse_mode=ParseMode.HTML)
    location_keyboard = KeyboardButton(text="Отправить местоположение",
                                       request_location=True)  # creating location button object
    custom_keyboard = [[location_keyboard]]  # creating keyboard object
    reply_markup = ReplyKeyboardMarkup(custom_keyboard,one_time_keyboard=True,resize_keyboard=True)
    context.bot.send_message(update.effective_chat.id,
                             "Разрешите доступ к местоположению, чтобы показывать данные о погоде.",
                             reply_markup=reply_markup)


def location(update: Update, context: CallbackContext) -> None:
    context.user_data['loc'] = update.effective_message.location
    context.bot.send_message(update.effective_chat.id, 'Данные местоположения успешно получены!')
