# Telegram API Libraries
from telegram.ext import CommandHandler

# Starting message for Bot
async def start(update, context):
    pass

start_handler = CommandHandler("start", start)