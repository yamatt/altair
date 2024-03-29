from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, Request, Response

from telegram import Update

from bot import bot
from secrets import Secrets
from log import log

webhook = FastAPI()


@asynccontextmanager
async def lifespan(_: FastAPI):
    log.info("LIFESPAN")
    async with bot:
        await bot.start()
        yield
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
async def process_update(request: Request):
    log.info("WEBHOOK")
    req = await request.json()
    update = Update.de_json(req, bot.bot)
    await bot.process_update(update)
    return Response(status_code=HTTPStatus.OK)
