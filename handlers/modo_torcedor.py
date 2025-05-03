from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from handlers.menu import menu_principal

async def menu_modo_torcedor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🧠 Quiz do Dia", "🔮 Palpite do Jogo", "🔫 Melhores momentos"],
        ["⬅️ Voltar"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🔥 Bem-vindo ao Modo Torcedor!\nEscolha uma opção:", reply_markup=reply_markup)

async def voltar_ao_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Você voltou ao menu principal.",
        reply_markup=menu_principal()
    )


