from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup  # type: ignore
from telegram.ext import ContextTypes  # type: ignore
from utils import buscar_proximos_jogos, buscar_ultimos_resultados
from textos import historia_furia, lineup_furia
from notificacoes import adicionar_usuario, remover_usuario

def menu_principal():
    teclado = [
        ["🎯 Line-up"],
        ["📅 Ver próximas partidas"],
        ["✅ Últimos resultados"],
        ["📰 Notícias"],
        ["📖 Nossa história"],
        ["🔔 Ativar notificações", "🔕 Desativar notificações"]
    ]
    return ReplyKeyboardMarkup(teclado, resize_keyboard=True)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bem-vindo ao bot FURIOSO! \nO bot exclusivo para nossa equipe de CS2.\nPara continuar, escolha uma das opções abaixo:",
        reply_markup=menu_principal()
    )

# responde qualquer mensagem enviando o menu
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    chat_id = update.message.chat_id

    if texto == "📅 Ver próximas partidas":
        resposta = buscar_proximos_jogos()
        await update.message.reply_text(f"{resposta}")

    elif texto == "✅ Últimos resultados":
        resposta = buscar_ultimos_resultados()
        await update.message.reply_text(f"{resposta}")

    elif texto == "📖 Nossa história":
        await update.message.reply_text(historia_furia)

    elif texto == "🎯 Line-up":
        await update.message.reply_text(lineup_furia, reply_markup=menu_principal())

    elif texto == "📰 Notícias":
        link_noticias = "https://draft5.gg/equipe/330-FURIA/noticias"
        resposta = f"Veja as ultimas notícias da FURIA aqui: {link_noticias}"
        await update.message.reply_text(resposta, reply_markup=menu_principal())

    elif texto == "🔔 Ativar notificações":
        adicionar_usuario(chat_id)
        await update.message.reply_text("✅ Notificações ativadas! Você receberá alertas dos jogos da FURIA.")

    elif texto == "🔕 Desativar notificações":
        remover_usuario(chat_id)
        await update.message.reply_text("🔕 Notificações desativadas. Você não receberá mais alertas.")

    else:
        await update.message.reply_text(
            "Bem-vindo ao bot FURIOSO! \nNosso bot exclusivo para assuntos de nossa equipe de CS2.\nPara continuar, escolha uma das opções abaixo:",
            reply_markup=menu_principal()
        )