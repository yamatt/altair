import os

class Secrets:
    TELEGRAM_API_TOKEN: str = os.environ.get("TELEGRAM_API_TOKEN")