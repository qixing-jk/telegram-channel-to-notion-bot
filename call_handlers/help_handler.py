from telegram import Update
from telegram.ext import ContextTypes

from logger import log


@log
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I am a robot, can i help you?")
