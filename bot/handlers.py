from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup  # type: ignore
from telegram.ext import ContextTypes  # type: ignore
from bot.utils import buscar_proximos_jogos, buscar_ultimos_resultados
from bot.textos import historia_furia, lineup_furia

def menu_principal():
    teclado = [
        ["🎯 Line-up"],
        ["📅 Ver próximas partidas"],
        ["✅ Últimos resultados"],
        ["📰 Notícias"],
        ["📖 Nossa história"]
    ]
    return ReplyKeyboardMarkup(teclado, resize_keyboard=True)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bem-vindo ao bot FURIOSO! \nO bot exclusivo para nossa equipe de CS2.\nPara continuar, escolha uma das opções abaixo:",
        reply_markup=menu_principal()
    )

# responde aos botoes inline
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'proximos_jogos':
        resposta = buscar_proximos_jogos()
        await query.edit_message_text(text=f"{resposta}")

    elif query.data == 'ultimos_resultados':
        resposta = buscar_ultimos_resultados()
        await query.edit_message_text(text=f"{resposta}")

    elif query.data == 'nossa_historia':
        await query.edit_message_text(text=f"Sobre nós:\n{historia_furia}")

    elif query.data == 'line_up':
        await query.edit_message_text(text=lineup_furia)

    elif query.data == 'noticias':
        link_noticias = "https://draft5.gg/equipe/330-FURIA/noticias"
        resposta = f"Veja as ultimas notícias da FURIA aqui: {link_noticias}"
        await query.edit_message_text(text=resposta)

    await query.message.reply_text( 
        "Escolha uma opção abaixo:",
        reply_markup=menu_principal()
    )

# responde qualquer mensagem enviando o menu
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text

    if texto == "📅 Ver próximas partidas":
        resposta = buscar_proximos_jogos()
        await update.message.reply_text(f"{resposta}")

    elif texto == "✅ Últimos resultados":
        resposta = buscar_ultimos_resultados()
        await update.message.reply_text(f"{resposta}")

    elif texto == "📖 Nossa história":
        await update.message.reply_text(
            "Somos FURIA. Uma organização de esports que nasceu do desejo de representar o Brasil no CS e conquistou muito mais que isso: expandimos nossas ligas, disputamos os principais títulos, adotamos novos objetivos e ganhamos um propósito maior.\n"
            "Somos muito mais que o sucesso competitivo.\n"
            "Somos um movimento sociocultural.\n"
            "Nossa história é de pioneirismo, grandes conquistas e tradição. Nosso presente é de desejo, garra e estratégia. "
            "A pantera estampada no peito estampa também nosso futuro de glória. Nossos pilares de performance, lifestyle, "
            "conteúdo, business, tecnologia e social são os principais constituintes do movimento FURIA, que representa uma "
            "unidade que respeita as individualidades e impacta positivamente os contextos em que se insere. "
            "Unimos pessoas e alimentamos sonhos dentro e fora dos jogos."
        )

    elif texto == "🎯 Line-up":
        resposta = (
            "Line-up FURIOSA:\n"
            "KSCERATO\n"
            "Yuurih\n"
            "YEKINDAR\n"
            "FalleN\n"
            "MOLODOY\n\n"
            "Reservas:\n"
            "chelo\n"
            "skullz\n"
            "\nsidde (Coach)"
        )
        await update.message.reply_text(resposta, reply_markup=menu_principal())

    elif texto == "📰 Notícias":
        link_noticias = "https://draft5.gg/equipe/330-FURIA/noticias"
        resposta = f"Veja as ultimas notícias da FURIA aqui: {link_noticias}"
        await update.message.reply_text(resposta, reply_markup=menu_principal())

    else:
        await update.message.reply_text(
            "Bem-vindo ao bot FURIOSO! \nNosso bot exclusivo para assuntos de nossa equipe de CS2.\nPara continuar, escolha uma das opções abaixo:",
            reply_markup=menu_principal()
        )