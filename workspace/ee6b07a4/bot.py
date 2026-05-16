import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from filter_service import FilterService

load_dotenv()
logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
filter_service = FilterService()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check both text and captions
    text = update.message.text or update.message.caption
    
    if text and filter_service.is_profane(text):
        await update.message.delete()
        logging.info(f"Deleted message from {update.effective_user.id}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Filter text and captions
    msg_handler = MessageHandler(filters.TEXT | filters.CAPTION & (~filters.COMMAND), handle_message)
    application.add_handler(msg_handler)
    
    application.run_polling()