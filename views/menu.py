# encoding: utf-8


import requests
import pandas as pd
import numpy as np
import configurations.settings as settings
from typing import Dict
from utils.logger import get_logger
from utils.helpers import *
from telegram.ext import Dispatcher, CallbackContext
from telegram import Update, InlineKeyboardMarkup, Location
from telegram.ext import CommandHandler, CallbackQueryHandler
from connectors.db import log_to_db

# Init logger
logger = get_logger(__name__)
# States of menu
MONDAY = '0'
TUESDAY = '1'
WEDNESDAY = '2'
THURSDAY = '3'
FRIDAY = '4'
SATURDAY = '5'
SUNDAY = '6'
SHOW_SCHEDULE = '7'
DOWNLOAD_SCHEDULE = '8'
CHANGE_NOTIFY = '9'
NOWDAY = '10'
GET_WEATHER = '11'
DAYS = {MONDAY: 'Понедельник', TUESDAY: 'Вторник', WEDNESDAY: 'Среда', THURSDAY: 'Четверг', FRIDAY: 'Пятница',
        SATURDAY: 'Суббота', SUNDAY: 'Воскресенье', NOWDAY: 'Сегодня'}


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""

    dispatcher.add_handler(CommandHandler('menu', menu))
    dispatcher.add_handler(CallbackQueryHandler(callback))


@log_to_db
def menu(update: Update, context: CallbackContext) -> None:
    is_notify = update.effective_user.id in context.bot_data['notify_set']
    button_list = [
        InlineKeyboardButton("Просмотреть расписание", callback_data=SHOW_SCHEDULE),
        InlineKeyboardButton("Скачать расписание (csv файл)", callback_data=DOWNLOAD_SCHEDULE),
        InlineKeyboardButton(f"Уведомлять о предметах?  |{'Да' if is_notify else 'Нет'}", callback_data=CHANGE_NOTIFY),
        InlineKeyboardButton(f"Узнать погоду", callback_data=GET_WEATHER),
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    context.bot.send_message(update.effective_chat.id, 'Меню', reply_markup=reply_markup)

@log_to_db
def callback(update: Update, context: CallbackContext):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    # Stupid state machine realization
    if query.data == CHANGE_NOTIFY:
        is_notify = update.effective_user.id in context.bot_data['notify_set']
        if is_notify:
            context.bot_data['notify_set'].remove(update.effective_user.id)
        else:
            context.bot_data['notify_set'].add(update.effective_user.id)
        is_notify = not is_notify
        button_list = [
            InlineKeyboardButton("Просмотреть расписание", callback_data=SHOW_SCHEDULE),
            InlineKeyboardButton("Скачать расписание (csv файл)", callback_data=DOWNLOAD_SCHEDULE),
            InlineKeyboardButton(f"Уведомлять о предметах?  |{'Да' if is_notify else 'Нет'}",
                                 callback_data=CHANGE_NOTIFY),
            InlineKeyboardButton(f"Узнать погоду", callback_data=GET_WEATHER),
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
        query.edit_message_text('Меню', reply_markup=reply_markup)
    elif query.data == DOWNLOAD_SCHEDULE:
        query.edit_message_text('Пока не реализовано(', reply_markup=None)
    elif query.data == SHOW_SCHEDULE:
        button_list = [
            InlineKeyboardButton("1. Понедельник", callback_data=MONDAY),
            InlineKeyboardButton("2. Вторник", callback_data=TUESDAY),
            InlineKeyboardButton("3. Среда", callback_data=WEDNESDAY),
            InlineKeyboardButton("4. Четверг", callback_data=THURSDAY),
            InlineKeyboardButton("5. Пятница", callback_data=FRIDAY),
            InlineKeyboardButton("6. Суббота", callback_data=SATURDAY),
            InlineKeyboardButton("7. Воскресенье", callback_data=SUNDAY),
            InlineKeyboardButton("8. Сегодня", callback_data=NOWDAY),

        ]
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
        query.edit_message_text('Выберите день недели', reply_markup=reply_markup)
    elif query.data in DAYS:

        day = int(query.data)
        if str(day) == NOWDAY:
            day = pd.Timestamp.now().dayofweek
        schedule: pd.DataFrame = context.bot_data['schedule']
        day_time = pd.Timestamp.now()
        day_time -= pd.Timedelta((day_time.dayofweek - day), unit='D')
        # TODO
        schedule = schedule.loc[(schedule['start'].dt.dayofweek == day) & (
                np.mod((day_time.date() - schedule['start'].dt.date).dt.days, schedule['period']) == 0), :]
        message = f'\nЗанятия на {DAYS[query.data]}'
        if schedule.index.size == 0:
            message += "\nЗанятий нет!!!"
        else:
            idx = 1
            for i in schedule.index:
                lesson = schedule.loc[i, :]
                message += f"\n{idx}.  {lesson['name']} {lesson['teacher']} " \
                           f"{lesson['start'].strftime('%H:%M')}-{lesson['end'].strftime('%H:%M')}\n"
                idx += 1
        query.edit_message_text(message, reply_markup=None)
    elif query.data == GET_WEATHER:
        message = ''
        loc: Location = context.user_data.get('loc', None)
        if loc:
            try:
                weather = get_weather(loc.latitude, loc.longitude)
                buf_message = f'Текущая погода \n\n' \
                              f'Температура {weather["main"]["temp"]} °C\n' \
                              f'Ветер {weather["wind"]["speed"]} м/с\n' \
                              f'Облачность {weather["clouds"]["all"]}% \n'
                rain = weather.get('rain', None)
                if rain is not None:
                    rain = rain.get('1h', None)
                    if rain:
                        weather += f'Дождь {rain} мм \n'

                message += buf_message
            except Exception as e:
                logger.warning(str(e))
                message += 'Не удалось получить данные о погоде!'
        query.edit_message_text(message, reply_markup=None)


# Фокус со статической переменной, не повторять в домашних условиях!
def get_weather(lat: str, lon: str, s=requests.session()) -> Dict:
    key = settings.OPW_KEY
    r = s.get('http://api.openweathermap.org/data/2.5/weather',
              params={'lat': lat, 'lon': lon, 'appid': key, 'units': 'metric', })
    return r.json()
