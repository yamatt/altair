from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler
from telegram.ext._contexttypes import ContextTypes, ConversationHandler

from secrets import Secrets
from log import log
from post import Post


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

# States
WRITING = 1


async def send_processing_action(chat_id):
    await bot.send_chat_action(chat_id, ChatAction.TYPING)


async def start(update, _: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    log.info("BOT START")
    await update.message.reply_markdown(
        "Hello. Please type `/new <name>` to start a new post"
    )


async def new(update, context: ContextTypes.DEFAULT_TYPE):
    log.info("BOT NEW")
    send_processing_action(update.effective_message.chat_id)
    new_post = Post.from_telegram(context)
    await update.message.reply_markdown(
        f"Your new blog post title will be _{new_post.title}_ with branch name `{new_post.branch_name}`. Please start writing the blog post."
    )


async def writing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info("WRITING MODE", context=dict(context))

    send_processing_action(update.effective_message.chat_id)

    # update blog post

    return WRITING


paragraphs = ConversationHandler(
    entry_points=[CommandHandler("new", new)],
    states={WRITING: [MessageHandler(filters.Regex(".*"), writing)]},
    fallbacks=[CommandHandler("new", new)],
)

bot.add_handler(CommandHandler("start", start))
bot.add_handler(paragraphs)
