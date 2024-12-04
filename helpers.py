from telegram import Update
import re
from setup import logger

# List of allowed usernames
ALLOWED_HANDLES = ["jovvvvs", "jiaxinnns"]

# Check if the user is allowed
def is_user_allowed(update: Update) -> bool:
    username = update.message.from_user.username

    # log false attempts
    if username not in ALLOWED_HANDLES:
        logger.warning(f"Unauthorized access attempt by {username}")

    return username in ALLOWED_HANDLES

# Check if the email is valid
def is_valid_email(email):
    # Basic email validation
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)