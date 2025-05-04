import json
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from handlers.modo_torcedor import menu_modo_torcedor
from services.pandascore_api import obter_jogos_futuros
from utils.formatadores import formatar_jogo

RESPONDENDO_PALPITE, APOS_PALPITE = range(2)

def carregar_perguntas_palpite():
    try:
        with open('data/palpites.json', 'r', encoding='utf-8') as file:
            return json.load(file)['perguntas']
    except Exception as e:
        print(f"Erro ao carregar perguntas de palpite: {e}")
        return []

async def iniciar_palpite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jogos_futuros = obter_jogos_futuros()
    
    if not jogos_futuros:
        await update.message.reply_text(
            "🔍 Não encontrei nenhum jogo agendado para a FURIA no momento.\n"
            "Tente novamente mais tarde ou volte ao menu principal.",
            reply_markup=ReplyKeyboardMarkup([["⬅️ Voltar ao Modo Torcedor"]], resize_keyboard=True)
        )
        return ConversationHandler.END
    
    proximo_jogo = jogos_futuros[0]
    
    jogo_formatado = formatar_jogo(proximo_jogo)
    await update.message.reply_text(
        f"🚨 Hora do Duelo!\n\n{jogo_formatado}"
    )
    
    perguntas = carregar_perguntas_palpite()
    if not perguntas:
        await update.message.reply_text(
            "Desculpe, não consegui carregar as perguntas de palpite. Tente novamente mais tarde.",
            reply_markup=ReplyKeyboardMarkup([["⬅️ Voltar ao Modo Torcedor"]], resize_keyboard=True)
        )
        return ConversationHandler.END
    
    pergunta = random.choice(perguntas)
    context.user_data['pergunta_palpite'] = pergunta
    
    oponentes = proximo_jogo["opponents"]
    time_furia = next((op["opponent"]["name"] for op in oponentes if op["opponent"]["id"] == 124530), "FURIA")
    time_adversario = next((op["opponent"]["name"] for op in oponentes if op["opponent"]["id"] != 124530), "Adversário")
    
    context.user_data['time_furia'] = time_furia
    context.user_data['time_adversario'] = time_adversario
    
    keyboard = [
        [time_furia],
        [time_adversario],
        ["⬅️ Voltar ao Modo Torcedor"]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        f"🔮 {pergunta['pergunta'].format(time_furia=time_furia, time_adversario=time_adversario)}",
        reply_markup=reply_markup
    )
    
    return RESPONDENDO_PALPITE

async def processar_palpite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resposta = update.message.text
    
    if resposta == "⬅️ Voltar ao Modo Torcedor":
        await menu_modo_torcedor(update, context)
        return ConversationHandler.END
    
    time_furia = context.user_data.get('time_furia', 'FURIA')
    time_adversario = context.user_data.get('time_adversario', 'Adversário')
    pergunta = context.user_data.get('pergunta_palpite', {})
    
    keyboard = [
        ["🎮 Fazer outro palpite"],
        ["⬅️ Voltar ao Modo Torcedor"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    if resposta == time_furia:
        await update.message.reply_text(
            f"🔥 BOA FURIOSO! TAMO JUNTO! 🔥\n\n"
            f"Seu palpite foi registrado! Você acredita que {time_furia} vai {pergunta.get('acao', 'vencer')}!",
            reply_markup=reply_markup
        )
    elif resposta == time_adversario:
        await update.message.reply_text(
            f"👀 ESTAMOS DE OLHO EM VOCÊ, HEIN? 👀\n\n"
            f"Seu palpite foi registrado! Você acredita que {time_adversario} vai {pergunta.get('acao', 'vencer')}!\n"
            f"Mas a FURIA vai mostrar seu verdadeiro poder! 🔥",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "Resposta não reconhecida. Vamos tentar novamente?",
            reply_markup=reply_markup
        )
    
    return APOS_PALPITE

async def apos_palpite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resposta = update.message.text
    
    if resposta == "🎮 Fazer outro palpite":
        return await iniciar_palpite(update, context)
    elif resposta == "⬅️ Voltar ao Modo Torcedor":
        await menu_modo_torcedor(update, context)
        return ConversationHandler.END
    else:
        await menu_modo_torcedor(update, context)
        return ConversationHandler.END
        
async def encerrar_palpite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await menu_modo_torcedor(update, context)
    return ConversationHandler.END