from enum import Enum, auto

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from secrets import Secrets
from config import Config
from log import log
from post import Post, Paragraph

from repo import Repo


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")


repo = Repo(Config, Secrets)

bot = (
    Application.builder()
    .updater(None)
    .token(Secrets.TELEGRAM_API_TOKEN)
    .read_timeout(7)
    .get_updates_read_timeout(42)
    .build()
)


class States(Enum):
    WRITING = auto()


async def send_processing_action(chat_id):
    await bot.bot.send_chat_action(chat_id, ChatAction.TYPING)


async def start(update, _: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    log.info("BOT START")
    await update.message.reply_markdown(
        "Hello. Please type `/new <name>` to start a new post"
    )


async def new(update, context: ContextTypes.DEFAULT_TYPE):
    log.info("BOT NEW")
    await send_processing_action(update.effective_message.chat_id)
    new_post = Post.from_telegram(context)

    context.chat_data["post"] = new_post

    repo.create_branch(new_post.branch_name)

    await update.message.reply_markdown(
        f"Your new blog post title will be _{new_post.title}_ with branch name `{new_post.branch_name}`. Please start writing the blog post."
    )
    return States.WRITING


async def text(update, context: ContextTypes.DEFAULT_TYPE):
    log.info("WRITING TEXT")

    await update.message.reply_text(context.chat_data["post"].text())
    return States.WRITING


async def writing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(
        "WRITING MODE",
        message_id=update.message.message_id,
        message_text=update.message.text,
    )

    await send_processing_action(update.effective_message.chat_id)

    if context.chat_data.get("post"):
        context.chat_data["post"].add_paragraph(Paragraph.from_update(update))
        repo.update_post(context.chat_data["post"])

    else:
        await update.message.reply_markdown(
            f"No new post found. You will have to start a new one."
        )

    return States.WRITING


paragraphs = ConversationHandler(
    entry_points=[CommandHandler("new", new)],
    states={States.WRITING: [MessageHandler(filters.Regex(r"^[^\/].*$"), writing)]},
    fallbacks=[CommandHandler("new", new), CommandHandler("text", text)],
)

bot.add_handler(CommandHandler("start", start))
bot.add_handler(paragraphs)
