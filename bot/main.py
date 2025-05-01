import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from telegram.ext import Application, CommandHandler, MessageHandler, filters  # type: ignore
from handlers import start, responder
from auth import TOKEN
from scheduler import iniciar_scheduler

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))

    iniciar_scheduler(application)

    application.run_polling()

if __name__ == "__main__":
    main()