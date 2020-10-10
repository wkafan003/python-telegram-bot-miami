# encoding: utf-8

# Telegram API framework core imports
import time
import schedule
from telegram.ext import Dispatcher, CallbackContext
import threading
from utils.logger import get_logger

# Init logger
logger = get_logger(__name__)


def job():
    print(1)


def init(dispatcher: Dispatcher):
    schedule.every(2).seconds.do(job)
    t = threading.Thread(target=schedule_check, daemon=True).start()



def schedule_check():
    while True:
        schedule.run_pending()
        time.sleep(1)
