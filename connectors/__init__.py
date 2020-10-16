import logging
import psycopg2.extensions
import psycopg2
import configurations.settings as setting

conn: psycopg2.extensions.connection

# Init logger
logger = logging.getLogger(__name__)

try:
    conn = psycopg2.connect(
        f"dbname='{setting.DB_OPTIONS['dbname']}' user='{setting.DB_OPTIONS['user']}' "
        f"host='{setting.DB_OPTIONS['host']}' password='{setting.DB_OPTIONS['password']}'"
        f"port= {setting.DB_OPTIONS['port']}")
except psycopg2.OperationalError as e:
    logger.error(f'Unable to connect to db. {e}')
    raise
except Exception as e:
    logger.error(f'Unexpected error. {e}')
    raise
