# Telegram API Libraries
from telegram.ext import CommandHandler, ConversationHandler


# End the conversation
async def cancel(update, context):
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

cancel_handler = CommandHandler("cancel", cancel)