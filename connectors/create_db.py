import logging
from . import conn

# Init logger
logger = logging.getLogger(__name__)


def create_db(path):
    with open(path, 'r') as f:
        ddl = f.read()
        try:
            cur = conn.cursor()
            cur.execute(ddl)
            conn.commit()
            cur.close()
        except Exception as e:
            logger.error(f'Unable to create db.{e}')
            raise
