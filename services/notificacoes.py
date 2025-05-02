from data.usuarios import obter_usuarios, salvar_usuario
from services.pandascore_api import obter_jogos_futuros
from datetime import datetime, timedelta
from telegram.ext import Application
import pytz

avisos_enviados = set()

def adicionar_usuario(chat_id):
    usuarios = obter_usuarios()  
    if chat_id not in usuarios:
        usuarios.append(chat_id)
        salvar_usuario(usuarios) 

def remover_usuario(chat_id):
    usuarios = obter_usuarios() 
    if chat_id in usuarios:
        usuarios.remove(chat_id) 
        salvar_usuario(usuarios) 

def verificar_e_enviar_notificacoes(application: Application):
    jogos = obter_jogos_futuros() 
    usuarios = obter_usuarios()  

    agora = datetime.now(pytz.utc)

    for jogo in jogos:
        if not jogo["scheduled_at"]:
            continue

        horario_jogo = datetime.fromisoformat(jogo["scheduled_at"].replace("Z", "+00:00"))
        delta = horario_jogo - agora

        # aviso 30 min
        if timedelta(minutes=29) < delta <= timedelta(minutes=31):
            mensagem = f"⚠️ A FURIA joga em 30 minutos contra {jogo['opponent']}!"
            if (jogo["opponent"], "30min") not in avisos_enviados:
                for user_id in usuarios:
                    application.bot.send_message(chat_id=user_id, text=mensagem)
                avisos_enviados.add((jogo["opponent"], "30min"))

        # aviso inicio 
        if timedelta(seconds=-30) < delta <= timedelta(seconds=30):
            mensagem = f"🔥 A FURIA está jogando agora contra {jogo['opponent']}! Bora torcer! #DaleFURIA"
            if (jogo["opponent"], "inicio") not in avisos_enviados:
                for user_id in usuarios:
                    application.bot.send_message(chat_id=user_id, text=mensagem)
                avisos_enviados.add((jogo["opponent"], "inicio"))
