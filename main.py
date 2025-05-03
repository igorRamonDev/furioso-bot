from telegram.ext import Application, CommandHandler, MessageHandler, filters  # type: ignore
from handlers.menu import start, responder
from config.auth import TOKEN
from utils.scheduler import iniciar_scheduler
from handlers.modo_torcedor import menu_modo_torcedor
from handlers.modo_torcedor import voltar_ao_menu

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex("🐾 Modo torcedor"), menu_modo_torcedor))
    application.add_handler(MessageHandler(filters.Regex("⬅️ Voltar"), voltar_ao_menu))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))


    iniciar_scheduler(application)
    application.run_polling()

if __name__ == "__main__":
    main()
