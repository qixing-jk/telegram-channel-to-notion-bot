import asyncio
import os
from typing import Optional

from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes

import logging
from call_handlers.message_handler import listen_message
from call_handlers.start_handler import start

from call_handlers.help_handler import help

start_handler = CommandHandler('start', start)
test_handler = CommandHandler('help', help)
message_handler = MessageHandler(filters.ALL, listen_message)

handlers_list = [
    start_handler,
    test_handler,
    message_handler,
]


async def error_handler(update: Optional[object], context: ContextTypes.DEFAULT_TYPE):
    error = context.error
    # 如果聊天限制了 bot 发送消息, 忽略
    if error.__class__.__name__ == "BadRequest":
        if error.message == "Chat_write_forbidden":
            return
    logging.error(f"在该更新发生错误\n{update}\n错误信息\n{error.__class__.__name__}:{error}")
    if context.bot_data.get("error_notice", False):
        async def send_update_error(chat_id):
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"在该更新发生错误\n{update}\n错误信息\n\n{context.error.__class__.__name__}:{context.error}",
            )
        tasks = [send_update_error(chat_id) for chat_id in os.getenv('owners')]
        await asyncio.gather(*tasks)
