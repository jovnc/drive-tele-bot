# Telegram API Libraries
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler

# Misc Libraries
from helpers import is_user_allowed, is_valid_email
from commands.cancel import cancel
from setup import logger, drive_service, SELECT_FOLDERS, ENTER_EMAIL, folders

# Share a folder
def share_folder(folder_id, email):
    permission = {
        'type': 'user',
        'role': 'reader',
        'emailAddress': email
    }
    try:
        drive_service.permissions().create(fileId=folder_id, body=permission, fields='id').execute()
        print(f"Folder shared successfully with {email}")
    except Exception as e:
        print(f"Error sharing folder: {e}")

# Start the conversation with /share
async def start_share(update, context):
    # Check if user is allowed to use the bot
    if not is_user_allowed(update):
        await update.message.reply_text("You are not authorized to use this bot.")
        return ConversationHandler.END

    message = (
        "💡 *How to Use /share Command* 💡\n\n"
        "🚀 *`/share`*:\n"
        "Want to share *just one file* with someone? Here's how:\n"
        "1️⃣ *Send the email address* of the person you want to share with. ✉️\n"
        "2️⃣ *Select the folder* containing the file you want to share. 📂\n"
        "3️⃣ Done! Your selected file will be sent to the email you provided. ✅\n\n"
        "📌 *Pro Tips*:\n"
        "- Double-check the email before submitting! ✅\n"
        "- Use *`/cancel`* anytime to stop or reset the process. 🛑\n\n"
        "Ready to start sharing? Give it a try now! 💌✨"
    )

    await update.message.reply_text(
        text=message,
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )
    
    await update.message.reply_text(
        "Email address (in full @gmail.com format):",
    )

    return ENTER_EMAIL

async def enter_email(update, context):

    email = update.message.text
    context.user_data["email"] = email

    if not is_valid_email(email):
        await update.message.reply_text("Invalid email. Please try again.")
        return ENTER_EMAIL

    context.user_data["email"] = email

    keyboard = [[InlineKeyboardButton(folder[0], callback_data=folder[1])] for folder in folders]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(f"Email selected: {email} \n\nSelect folders to share:", reply_markup=reply_markup)

    return SELECT_FOLDERS

    

async def enter_folder(update, context):

    try: 
        query = update.callback_query
        await query.answer() 
        folder_id = query.data 
        context.user_data["folder_id"] = folder_id
        email = context.user_data["email"]

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Sharing folder with ID {folder_id} with {email}..."
        )

        # share folder with user
        share_folder(folder_id, email)

        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Folder shared successfully with {email}..."
        )
        
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error sharing folder: {e}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Error sharing folder. Please try again."
        )


# Conversation handler
share_handler = ConversationHandler(
    entry_points=[CommandHandler("share", start_share)],
    states={
        ENTER_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_email)],
        SELECT_FOLDERS: [CallbackQueryHandler(enter_folder)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    per_message=False,
)