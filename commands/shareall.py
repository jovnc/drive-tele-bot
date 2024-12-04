from commands.share import share_folder

# Telegram API Libraries
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler

# Misc Libraries
from helpers import is_user_allowed, is_valid_email
from commands.cancel import cancel
from setup import SELECT_FOLDERS, ENTER_EMAIL, folders, logger

selected_options = {}

# Start the conversation with /share
async def start_share_all(update, context):
    # Check if user is allowed to use the bot
    if not is_user_allowed(update):
        await update.message.reply_text("You are not authorized to use this bot.")
        return ConversationHandler.END

    message = (
        "💡 *How to Use /shareall Command* 💡\n\n"
        "🌟 *`/shareall`*:\n"
        "Need to share *multiple files*? This command has you covered!\n"
        "1️⃣ *Send the email address* of the recipient. ✉️\n"
        "2️⃣ *Choose multiple folders* that contain the files you want to share. "
        "You can select as many as you need! 📂📂📂\n"
        "3️⃣ Hit *Submit*, and all your selected files will be shared with the email provided. ✅\n\n"
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

def get_base_keyboard():
    keyboard = [[InlineKeyboardButton(folder[0], callback_data=folder[1])] for folder in folders]
    keyboard.append([InlineKeyboardButton("Submit", callback_data="submit")])
    return InlineKeyboardMarkup(keyboard)

async def get_updated_keyboard(selected):
    keyboard = []
    logger.info(selected)
    for i in range(len(folders)):
        text = f"{folders[i][0]}" + (" ✔" if folders[i][1] in selected else "")
        keyboard.append([InlineKeyboardButton(text, callback_data=folders[i][1])])
    keyboard.append([InlineKeyboardButton("Submit", callback_data='submit')])
    return InlineKeyboardMarkup(keyboard)


async def enter_email(update, context):

    email = update.message.text

    if not is_valid_email(email):
        await update.message.reply_text("Invalid email. Please try again.")
        return ENTER_EMAIL

    context.user_data["email"] = email

    await update.message.reply_text(f"Email selected: {email} \n\nSelect folders to share:", reply_markup=get_base_keyboard())

    return SELECT_FOLDERS

async def enter_folders(update, context):
    query = update.callback_query
    await query.answer() 
    user_id = query.from_user.id

    # Handle submission
    if query.data == 'submit':
        if user_id in selected_options and selected_options[user_id]:
            
            try: 
                email = context.user_data["email"]
                for option in selected_options[user_id]:

                    email = context.user_data["email"]

                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Sharing folder with ID: {option} with {email}..."
                    )

                    # share folder with user
                    share_folder(option, email)

                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"All folders shared successfully with {email}..."
                )
                
                # Clear cache
                selected_options[user_id] = []
                return ConversationHandler.END
            except Exception as e:
                logger.error(f"Error sharing folder: {e}")
                await query.edit_message_text("Error sharing folder. Please try again")
        else:
            await query.edit_message_text("You didn't select any options, command cancelled.")
            return ConversationHandler.END
        return

    # Track user selections
    if user_id not in selected_options:
        selected_options[user_id] = []
    if query.data not in selected_options[user_id]:
        selected_options[user_id].append(query.data)
    else:
        selected_options[user_id].remove(query.data)

    # Update the keyboard to reflect current selections
    markup = await get_updated_keyboard(selected_options[user_id])
    await query.edit_message_reply_markup(reply_markup=markup )


# Conversation handler
share_all_handler = ConversationHandler(
    entry_points=[CommandHandler("shareall", start_share_all)],
    states={
        ENTER_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_email)],
        SELECT_FOLDERS: [CallbackQueryHandler(enter_folders)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    per_message=False,
)