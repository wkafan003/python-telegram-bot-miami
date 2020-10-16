from typing import Dict

TOKEN = "TOKEN"
NAME = "miami_bot"
WEBHOOK = False
# Db configuration
DB_OPTIONS: Dict[str, str] = {
    'dbname': 'postgres',
    'user': 'postgres',
    'host': '127.0.0.1',
    'port': '5432',
    'password': 'PASSWORD',
}
## The following configuration is only needed if you setted WEBHOOK to True
WEBHOOK_OPTIONS = {
    'listen': '0.0.0.0',  # IP
    'port': 443,
    'url_path': TOKEN,  # This is recommended for avoiding random people
    # making fake updates to your views
}
WEBHOOK_URL = f'https://example.com/{WEBHOOK_OPTIONS["url_path"]}'
OPW_KEY = 'TOKEN'
