from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, Request, Response

from bot import bot

webhook = FastAPI()


@asynccontextmanager
async def lifespan(webhook: FastAPI):
    async with bot:
        await bot.start()
        yield
        await bot.stop()


@webhook.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@webhook.post("/")
async def process_update(request: Request):
    req = await request.json()
    update = Update.de_json(req, bot.bot)
    await bot.process_update(update)
    return Response(status_code=HTTPStatus.OK)
