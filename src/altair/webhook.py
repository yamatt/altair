from typing import Generator
from http import HTTPStatus

from fastapi import FastAPI, Depends, Request, Response

from telegram import Update
from telegram.ext import Application

from bot import bot
from secrets import Secrets
from log import log

webhook = FastAPI()


async def initialise_bot(_: FastAPI) -> Generator:
    log.info("INITIALISED BOT")
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
    await bot.bot.set_webhook(Secrets.TELEGRAM_WEBHOOK_URL)
    return {"status": "ok"}


@webhook.post("/")
async def process_update(
    request: Request, initialised_bot: Application = Depends(initialise_bot)
):
    log.info("WEBHOOK")
    req = await request.json()
    update = Update.de_json(req, initialised_bot.bot)
    await initialised_bot.process_update(update)
    return Response(status_code=HTTPStatus.OK)
