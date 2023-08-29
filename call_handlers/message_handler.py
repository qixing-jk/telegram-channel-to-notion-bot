from pprint import pprint

from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ContextTypes

from logger import log
from notion_service import generate_bookmark_block, generate_link_text_block, generate_date_text_block, \
    generate_heading_block, append_block, generate_text_block

channel_link = ""


@log
async def listen_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.chat.type == ChatType.CHANNEL:
        global channel_link
        channel_link = f"https://t.me/{update.effective_message.chat.username}"
        message_link = f"https://t.me/{update.effective_message.chat.username}/{update.effective_message.message_id}"
        pprint(update.effective_message)
        add_block_list = [
            generate_heading_block(2, generate_link_text_block(update.effective_message.chat.title, channel_link),
                                   generate_text_block(" ("),
                                   generate_date_text_block(update.effective_message.date), generate_text_block(")")),
            generate_bookmark_block(None, message_link)]
        pprint(add_block_list)
        append_block(add_block_list)
