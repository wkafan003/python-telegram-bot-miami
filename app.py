# coding: utf-8
import signal
import sys
import os

from telegram.ext import Updater, Dispatcher, PicklePersistence
from importlib import import_module

import utils.logger as logger
import configurations.settings as settings
import pandas as pd
import numpy as np


def load_handlers(dispatcher: Dispatcher):
    """Load handlers from files in a 'views' directory."""
    base_path = os.path.join(os.path.dirname(__file__), 'views')
    files = os.listdir(base_path)

    for file_name in files:
        handler_module, _ = os.path.splitext(file_name)
        if handler_module[:2] + handler_module[-2:] != '____':
            module = import_module(f'.{handler_module}', 'views')
            module.init(dispatcher)


def graceful_exit(*args, **kwargs):
    """Provide a graceful exit from a webhook server."""
    if updater is not None:
        updater.bot.delete_webhook()

    sys.exit(1)


if __name__ == "__main__":
    global updater
    logger.init_logger(f'logs/{settings.NAME}.log')
    persistence = PicklePersistence(filename='assets/data.pickle')
    updater = Updater(token=settings.TOKEN, persistence=persistence, use_context=True)
    # Set of notifiable users
    if updater.dispatcher.bot_data.get('notify_set', None) is None:
        updater.dispatcher.bot_data['notify_set'] = set()

    schedule = pd.read_csv('assets/schedule.csv').astype(
        {'name': 'string', 'teacher': 'string', 'start': np.datetime64, 'end': np.datetime64, 'period': np.uint8})
    updater.dispatcher.bot_data['schedule'] = schedule
    load_handlers(updater.dispatcher)

    if settings.WEBHOOK:
        signal.signal(signal.SIGINT, graceful_exit)
        updater.start_webhook(**settings.WEBHOOK_OPTIONS)
        updater.bot.set_webhook(url=settings.WEBHOOK_URL)
    else:
        updater.start_polling()
