import logging

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes

from settings import TOKEN

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


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.exception(f"got exception: {e}")
