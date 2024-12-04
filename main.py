from setup import app
from commands.cancel import cancel_handler
from commands.start import start_handler
from commands.share import share_handler
from commands.shareall import share_all_handler

def main():
    print("Bot started")

    # Add command handlers
    app.add_handler(start_handler)
    app.add_handler(share_handler)
    app.add_handler(cancel_handler)
    app.add_handler(share_all_handler)

    # Start the bot, poll every 10s
    app.run_polling(poll_interval=5, timeout=10, drop_pending_updates=True)

if __name__ == "__main__":
    main()