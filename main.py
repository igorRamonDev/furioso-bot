from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler # type: ignore
from handlers.menu import start, responder
from config.auth import TOKEN
from utils.scheduler import iniciar_scheduler
from handlers.modo_torcedor import menu_modo_torcedor, voltar_ao_menu
from handlers.quiz import (
    iniciar_quiz, processar_resposta, proxima_acao, encerrar_quiz, apos_ver_pontuacao,
    RESPONDENDO, MOSTRAR_RESULTADO, VER_PONTUACAO
)

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    
    quiz_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("🧠 Quiz"), iniciar_quiz)],
        states={
            RESPONDENDO: [MessageHandler(filters.TEXT & ~filters.COMMAND, processar_resposta)],
            MOSTRAR_RESULTADO: [MessageHandler(filters.TEXT & ~filters.COMMAND, proxima_acao)],
            VER_PONTUACAO: [MessageHandler(filters.TEXT & ~filters.COMMAND, apos_ver_pontuacao)]
        },
        fallbacks=[
            MessageHandler(filters.Regex("⬅️ Voltar ao Modo Torcedor"), encerrar_quiz),
            CommandHandler("start", start)
        ],
        name="quiz_conversation",
        persistent=False
    )
    application.add_handler(quiz_conv_handler)
    
    application.add_handler(MessageHandler(filters.Regex("🐾 Modo torcedor"), menu_modo_torcedor))
    application.add_handler(MessageHandler(filters.Regex("⬅️ Voltar"), voltar_ao_menu))
    
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))
    
    iniciar_scheduler(application)
    
    application.run_polling()

if __name__ == "__main__":
    main()