import logging
import time
from multiprocessing import Process

import requests
import uvicorn
from fastapi import FastAPI
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes

from settings import TOKEN

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def modify_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.channel_post.text
    logger.info(f"get message: {message_text}")

    if "www.instagram.com/" in message_text:
        modified_link = message_text.replace("instagram.com", "ddinstagram.com")
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.channel_post.message_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=modified_link)


def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    logger.info("bot started")
    application.add_handler(MessageHandler(filters.TEXT & filters.Entity("url"), modify_link))
    application.run_polling()


def server() -> None:
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")


def check_server() -> None:
    while True:
        try:
            rsp = requests.get("https://tg-bot-links-replacer.onrender.com")
        except Exception:
            logger.error("check server error")
        else:
            logger.info(f"response: {rsp.text}")
        finally:
            time.sleep(90)


if __name__ == '__main__':
    try:
        bot = Process(target=main)
        server = Process(target=server)
        checker = Process(target=check_server)
        bot.start()
        server.start()
        checker.start()
        bot.join()
        server.join()
        checker.join()
    except Exception as e:
        logger.exception(f"got exception: {e}")
