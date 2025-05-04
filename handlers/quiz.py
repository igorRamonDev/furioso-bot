import json
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from handlers.menu import menu_principal
from handlers.modo_torcedor import menu_modo_torcedor

RESPONDENDO, MOSTRAR_RESULTADO, VER_PONTUACAO = range(3)

pontuacao_usuarios = {}

def carregar_perguntas():
    try:
        with open('data/quiz_perguntas.json', 'r', encoding='utf-8') as file:
            return json.load(file)['perguntas']
    except Exception as e:
        print(f"Erro ao carregar perguntas: {e}")
        return []

async def iniciar_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    context.user_data['em_quiz'] = True
    
    if user_id not in pontuacao_usuarios:
        pontuacao_usuarios[user_id] = 0
    
    perguntas = carregar_perguntas()
    if not perguntas:
        await update.message.reply_text(
            "Desculpe, não consegui carregar as perguntas do quiz. Tente novamente mais tarde."
        )
        return ConversationHandler.END
    
    pergunta_atual = random.choice(perguntas)
    context.user_data['pergunta_atual'] = pergunta_atual
    
    #cria o teclado com opcoes
    opcoes = pergunta_atual['opcoes']
    keyboard = []
    for opcao in opcoes:
        keyboard.append([opcao])
    
    #adiciona pontuacao e voltar
    keyboard.append(["🏆 Ver Pontuação"])
    keyboard.append(["⬅️ Voltar ao Modo Torcedor"])
    
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    #envia a pergunta
    await update.message.reply_text(
        f"🧠 Pergunta: {pergunta_atual['pergunta']}",
        reply_markup=reply_markup
    )
    
    return RESPONDENDO

#processa a resposta do usuario
async def processar_resposta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    resposta = update.message.text
    
    if not context.user_data.get('em_quiz', False):
        return ConversationHandler.END
    
    if resposta == "🏆 Ver Pontuação":
        pontos = pontuacao_usuarios.get(user_id, 0)
        
        #teclado para apos ver pontuacao
        keyboard = [
            ["🎮 Próxima Pergunta"],
            ["🏆 Atualizar Pontuação"],
            ["⬅️ Voltar ao Modo Torcedor"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            f"🏆 Sua pontuação atual é: {pontos} pontos",
            reply_markup=reply_markup
        )
        return VER_PONTUACAO
    
    if resposta == "⬅️ Voltar ao Modo Torcedor":
        #limpa o estado de quiz
        context.user_data['em_quiz'] = False
        context.user_data.pop('pergunta_atual', None)
        await menu_modo_torcedor(update, context)
        return ConversationHandler.END
    
    pergunta_atual = context.user_data.get('pergunta_atual')
    if not pergunta_atual:
        await update.message.reply_text("Ocorreu um erro. Vamos recomeçar o quiz.")
        return await iniciar_quiz(update, context)
    
    resposta_correta = pergunta_atual['resposta_correta']
    curiosidade = pergunta_atual.get('curiosidade', '')
    
    keyboard = [
        ["🎮 Próxima Pergunta"],
        ["🏆 Ver Pontuação"],
        ["⬅️ Voltar ao Modo Torcedor"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    if resposta == resposta_correta:
        pontuacao_usuarios[user_id] = pontuacao_usuarios.get(user_id, 0) + 10
        await update.message.reply_text(
            f"✅ Excelente furioso! +10 pontos\n\n📝 {curiosidade}",
            reply_markup=reply_markup
        )
    else:
        pontuacao_usuarios[user_id] = max(0, pontuacao_usuarios.get(user_id, 0) - 10)  # Evita pontuação negativa
        await update.message.reply_text(
            f"❌ Erroooou! -10 pontos\n\nA resposta correta era: {resposta_correta}\n\n📝 {curiosidade}",
            reply_markup=reply_markup
        )
    
    return MOSTRAR_RESULTADO

async def proxima_acao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resposta = update.message.text
    
    if not context.user_data.get('em_quiz', False):
        return ConversationHandler.END
    
    if resposta == "🎮 Próxima Pergunta":
        return await iniciar_quiz(update, context)
    elif resposta == "🏆 Ver Pontuação":
        user_id = update.effective_user.id
        pontos = pontuacao_usuarios.get(user_id, 0)
        
        keyboard = [
            ["🎮 Próxima Pergunta"],
            ["🏆 Atualizar Pontuação"],
            ["⬅️ Voltar ao Modo Torcedor"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            f"🏆 Sua pontuação atual é: {pontos} pontos",
            reply_markup=reply_markup
        )
        return VER_PONTUACAO
    elif resposta == "⬅️ Voltar ao Modo Torcedor":
        context.user_data['em_quiz'] = False
        context.user_data.pop('pergunta_atual', None)
        await menu_modo_torcedor(update, context)
        return ConversationHandler.END
    else:
        return await iniciar_quiz(update, context)

async def apos_ver_pontuacao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resposta = update.message.text
    
    if not context.user_data.get('em_quiz', False):
        return ConversationHandler.END
    
    if resposta == "🎮 Próxima Pergunta":
        return await iniciar_quiz(update, context)
    elif resposta == "🏆 Atualizar Pontuação":
        user_id = update.effective_user.id
        pontos = pontuacao_usuarios.get(user_id, 0)
        
        keyboard = [
            ["🎮 Próxima Pergunta"],
            ["🏆 Atualizar Pontuação"],
            ["⬅️ Voltar ao Modo Torcedor"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            f"🏆 Sua pontuação atual é: {pontos} pontos",
            reply_markup=reply_markup
        )
        return VER_PONTUACAO
    elif resposta == "⬅️ Voltar ao Modo Torcedor":
        context.user_data['em_quiz'] = False
        context.user_data.pop('pergunta_atual', None)
        await menu_modo_torcedor(update, context)
        return ConversationHandler.END
    else:
        return await iniciar_quiz(update, context)

async def encerrar_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['em_quiz'] = False
    context.user_data.pop('pergunta_atual', None)
    
    await menu_modo_torcedor(update, context)
    return ConversationHandler.END