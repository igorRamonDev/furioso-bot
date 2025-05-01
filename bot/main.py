import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.handlers import button
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters  # type: ignore
from bot.handlers import start, button, responder
from auth import TOKEN

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))

    application.run_polling()

if __name__ == "__main__":
    main()