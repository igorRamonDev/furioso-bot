from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup  # type: ignore
from telegram.ext import ContextTypes  # type: ignore
from bot.utils import buscar_proximos_jogos

# Teclado normal
def menu_principal():
    teclado = [
        ["🎯 Line-up"],
        ["📅 Ver próximas partidas"],
        ["📖 Nossa história"]
    ]
    return ReplyKeyboardMarkup(teclado, resize_keyboard=True)

# /start (inline)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📅 Ver próximas partidas", callback_data='proximos_jogos')],
        [InlineKeyboardButton("📖 Nossa história", callback_data='nossa_historia')],
        [InlineKeyboardButton("🎯 Line-up", callback_data='line_up')]  # Corrigido o nome do callback_data
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Escolha uma opção:', reply_markup=reply_markup)

# Função que responde aos botões inline
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'proximos_jogos':
        resposta = buscar_proximos_jogos()
        await query.edit_message_text(text=f"Próximos jogos:\n{resposta}")

    elif query.data == 'nossa_historia':
        resposta = ("História da FURIA\n\nA FURIA Esports é uma organização brasileira de esports, "
                    "fundada em 2017. A equipe é conhecida por sua forte presença em jogos como Counter-Strike: "
                    "Global Offensive (CS:GO) e League of Legends (LoL). A FURIA conquistou diversos campeonatos e "
                    "se tornou uma das principais organizações de esports do Brasil.")
        await query.edit_message_text(text=f"Sobre nós:\n{resposta}")

    elif query.data == 'line_up':  # Corrigido o nome do callback_data
        resposta = (
            "Line-up FURIOSA:\n\n"
            "KSCERATO\n"
            "Yuurih\n"
            "YEKINDAR\n"
            "FalleN\n"
            "MOLODOY\n\n"
            "Reservas:\n"
            "chelo\n"
            "skullz\n"
        )
        await query.edit_message_text(text=resposta)  # Responde com o line-up

        # Envia o menu novamente após a resposta
        await query.message.reply_text(
            "Escolha uma opção abaixo:",
            reply_markup=menu_principal()
        )

# Função que responde qualquer mensagem e envia o menu
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text

    if texto == "📅 Ver próximas partidas":
        resposta = buscar_proximos_jogos()
        await update.message.reply_text(f"Próximos jogos:\n{resposta}")
    elif texto == "📖 Nossa história":
        await update.message.reply_text("Somos FURIA. Uma organização de esports que nasceu do desejo de representar o Brasil no CS e conquistou muito mais que isso: expandimos nossas ligas, disputamos os principais títulos, adotamos novos objetivos e ganhamos um propósito maior.\nSomos muito mais que o sucesso competitivo.\nSomos um movimento sociocultural.\nNossa história é de pioneirismo, grandes conquistas e tradição. Nosso presente é de desejo, garra e estratégia. A pantera estampada no peito estampa também nosso futuro de glória. Nossos pilares de performance, lifestyle, conteúdo, business, tecnologia e social são os principais constituintes do movimento FURIA, que representa uma unidade que respeita as individualidades e impacta positivamente os contextos em que se insere. Unimos pessoas e alimentamos sonhos dentro e fora dos jogos.")
    elif texto == "🎯 Line-up":
        resposta = (
            "Line-up FURIOSA:\n\n"
            "KSCERATO\n"
            "Yuurih\n"
            "YEKINDAR\n"
            "FalleN\n"
            "MOLODOY\n\n"
            "Reservas:\n"
            "chelo\n"
            "skullz\n"
        )
        await update.message.reply_text(resposta, reply_markup=menu_principal())  # Envia o menu de volta após a resposta
    else:
        # Se mandar qualquer outra coisa, reenvia o menu
        await update.message.reply_text(
            "Escolha uma opção abaixo:",
            reply_markup=menu_principal()
        )
