from telegram import Update, ReplyKeyboardMarkup # type: ignore
from telegram.ext import ContextTypes # type: ignore
from utils.formatadores import buscar_proximos_jogos, buscar_ultimos_resultados
from assets.txts.textos import historia_furia, lineup_furia
from services.notificacoes import adicionar_usuario, remover_usuario

def menu_principal():
    teclado = [
        ["🐾 Modo torcedor"],
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
    if 'em_quiz' in context.user_data:
        context.user_data.pop('em_quiz')
    if 'pergunta_atual' in context.user_data:
        context.user_data.pop('pergunta_atual')
        
    await update.message.reply_text(
        "🔥 FURIOSO chegou!\nO seu canal direto com tudo sobre a equipe de CS2 da FURIA.\nEscolha a sua próxima jogada e venha com a gente!",
        reply_markup=menu_principal()
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('em_quiz', False):
        return
        
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
        resposta = f"🔥 Fique ligado, torcedor FURIOSO!\n Veja o que está rolando com o time:\n 📢 {link_noticias}"
        await update.message.reply_text(resposta, reply_markup=menu_principal())
    elif texto == "🔔 Ativar notificações":
        adicionar_usuario(chat_id)
        await update.message.reply_text("✅ Notificações ativadas! Você receberá alertas dos jogos da FURIA.")
    elif texto == "🔕 Desativar notificações":
        remover_usuario(chat_id)
        await update.message.reply_text("🔕 Notificações desativadas. Você não receberá mais alertas.")
    else:
        await update.message.reply_text(
            "🔥 FURIOSO chegou!\nO seu canal direto com tudo sobre a equipe de CS2 da FURIA.\nEscolha a sua próxima jogada e venha com a gente!",
            reply_markup=menu_principal()
        )