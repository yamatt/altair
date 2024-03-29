import os


class Secrets:
    TELEGRAM_API_TOKEN: str = os.environ.get("TELEGRAM_API_TOKEN")
    TELEGRAM_WEBHOOK_URL: str = os.environ.get("TELEGRAM_WEBHOOK_URL")