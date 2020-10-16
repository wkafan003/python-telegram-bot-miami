import psycopg2
import psycopg2.extensions
import connectors
import logging
from datetime import datetime
from functools import wraps
from typing import Union
from . import conn

# Init logger
logger = logging.getLogger(__name__)


def log_action(user_id: Union[str, int], action: str, time: datetime):
    cur: psycopg2.extensions.cursor = conn.cursor()
    try:
        cur.execute("select count(*) from users where id=%s", (user_id,))
        if cur.fetchone()[0] == 1:
            cur.execute("insert into actions values (%s,%s,%s)", (user_id, action, time))
    except Exception as e:
        logger.warning(f"Unable to log action {action}, user_id: {user_id}, time: {time}. {e}")
    conn.commit()
    cur.close()


def insert_user(user_id: Union[str, int], name: str):
    cur: psycopg2.extensions.cursor = conn.cursor()
    try:
        cur.execute("select count(*) from users where id=%s", (user_id,))
        if cur.fetchone()[0] == 0:
            cur.execute("insert into users (id, name) values (%s,%s)", (user_id, name))
    except Exception as e:
        logger.warning(f"Unable to add user id: {user_id}, name: {name}. {e}")
    conn.commit()
    cur.close()


def log_to_db(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        action = func.__name__
        try:
            query = update.callback_query.data
            action += ' ' + query
        except:
            pass
        log_action(update.effective_user.id, action, datetime.now())
        return func(update, context, *args, **kwargs)

    return command_func
