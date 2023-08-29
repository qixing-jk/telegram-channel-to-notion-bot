from pprint import pprint

from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ContextTypes

from notion_service import NotionService
from logger import log
from telegram_service import process_telegram_message


# @log
async def listen_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.chat.type == ChatType.CHANNEL:
        process_telegram_message(update.effective_message)
        # NotionService().create_page(update.effective_message.text)
