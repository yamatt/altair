from typing import Generator
from http import HTTPStatus

from fastapi import FastAPI, Depends, Request, Response

from telegram import Update
from telegram.ext import Application

from bot import bot
from config import Config
from log import log

webhook = FastAPI()


# Dependency
async def get_bot():
    async with bot:
        await bot.start()
        yield bot
        await bot.stop()


@webhook.get("/healthcheck")
async def healthcheck():
    log.info("HEALTHCHECK")
    return {"status": "ok"}


@webhook.post("/setup")
async def setup():
    """
    Sets up Telegram for Webhooks
    """
    log.info("SETUP")
    await bot.bot.set_webhook(Config.TELEGRAM_WEBHOOK_URL)
    return {"status": "ok"}


@webhook.post("/")
async def process_update(
    request: Request, initialised_bot: Application = Depends(get_bot)
):
    log.info("WEBHOOK")
    req = await request.json()

    user_id: str = str(req["message"]["chat"]["id"])

    if user_id != Config.APPROVED_USER:
        # Ignore all messages that aren't from the approved user, return stub response.
        # We want to tell Telegram the payload is OK, just not the right user.
        log.info("USER ID INVALID", user_id=user_id)
        return Response(status_code=HTTPStatus.OK)

    update = Update.de_json(req, initialised_bot.bot)
    await initialised_bot.process_update(update)

    return Response(status_code=HTTPStatus.OK)
