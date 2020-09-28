from functools import wraps
import time
from typing import List, Optional

import telegram
from telegram import ChatAction, InlineKeyboardButton
from telegram.ext import Updater, Filters


def __send_response__(context: telegram.ext.CallbackContext) -> None:
    """
    Вспомогательная функция для send_typing_acton, которая отправляет сообщение по истечению duration
    :param context:
    """
    update: telegram.Update = context.job.context['update']
    if context.job.context['type'] == Filters.text:
        context.bot.send_message(update.effective_message.chat_id, context.job.context['message'],
                                 parse_mode=context.job.context.get('parse_mode', None))


def send_typing_action(duration: float = 0, action: ChatAction = ChatAction.TYPING):
    """
    Декоратор отправки сообщения с задержкой отправки и отправкой действия чата, на время этой задержки
    :param duration: Через какой время отправить ответ на сообщение
    :param action: Действие чата, отправляемое пользователю (по умолчанию набор текста)
    :return:
    """

    def layer(func):
        @wraps(func)
        def command_func(update: telegram.Update, context: telegram.ext.CallbackContext):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            t_start = time.time()
            res = func(update, context)
            t_end = time.time()
            job_q: telegram.ext.JobQueue = context.job_queue
            job_q.run_once(__send_response__, max(0.0, duration - (t_end - t_start)), context=res)
            return res

        return command_func

    return layer


def build_menu(buttons: List[InlineKeyboardButton],
               n_cols: int,
               header_buttons: Optional[InlineKeyboardButton] = None,
               footer_buttons: Optional[InlineKeyboardButton] = None) -> List[List[InlineKeyboardButton]]:
    """
    Создает встроенное меню, для пользователя телеграм
    :param buttons: Список кнопок InlineKeyboardButton.
    :param n_cols: Количество столбцов.
    :param header_buttons: Кнопка заголовок.
    :param footer_buttons: Кнопка футер.
    :return:
    """
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu
