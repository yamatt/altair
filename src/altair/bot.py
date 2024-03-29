from telegram import Update
from telegram.ext import Application, CommandHandler
from telegram.ext._contexttypes import ContextTypes

from secrets import Secrets
from log import log


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")


bot = (
    Application.builder()
    .updater(None)
    .token(Secrets.TELEGRAM_API_TOKEN)
    .read_timeout(7)
    .get_updates_read_timeout(42)
    .build()
)


async def start(update, _: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    log.info("BOT START")
    await update.message.reply_text("Hello. Please type `/new <name>` to start a new post")


async def new(update, context: ContextTypes.DEFAULT_TYPE):
    log.info("BOT NEW")
    title: str = " ".join(context.args)
    await update.message.reply_text(f"Your new blog post title will be _{title}_")


bot.add_handler(CommandHandler("start", start))
bot.add_handler(CommandHandler("new", new))
