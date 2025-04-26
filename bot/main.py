import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.handlers import button  # Agora deve funcionar

from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters  # type: ignore
from bot.handlers import start, button, responder
from auth import TOKEN

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))  # /start
    application.add_handler(CallbackQueryHandler(button))    # Botoes inline
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))  # Qualquer texto

    application.run_polling()

if __name__ == "__main__":
    main()
