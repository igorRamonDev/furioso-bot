from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from handlers.menu import menu_principal

async def menu_modo_torcedor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop('em_quiz', None)
    context.user_data.pop('pergunta_atual', None)
    
    keyboard = [
        ["🧠 Quiz", "🔮 Palpite do Jogo", "🔫 Melhores momentos"],
        ["⬅️ Voltar"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🔥 Bem-vindo ao Modo Torcedor!\nEscolha sua próxima jogada e venha torcer com a gente!", reply_markup=reply_markup)

async def voltar_ao_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop('em_quiz', None)
    context.user_data.pop('pergunta_atual', None)
    
    await update.message.reply_text(
        "🚨 Respawn concluído!\nVocê está no menu principal. Hora de decidir sua próxima jogada! 🎮🔥",
        reply_markup=menu_principal()
    )