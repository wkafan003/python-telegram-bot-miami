TOKEN = "TOKEN"
NAME = "miami_bot"
WEBHOOK = False
## The following configuration is only needed if you setted WEBHOOK to True ##
WEBHOOK_OPTIONS = {
    'listen': '0.0.0.0',  # IP
    'port': 443,
    'url_path': TOKEN,  # This is recommended for avoiding random people
                        # making fake updates to your views
}
WEBHOOK_URL = f'https://example.com/{WEBHOOK_OPTIONS["url_path"]}'
OPW_KEY = 'OPW_TOKEN'
