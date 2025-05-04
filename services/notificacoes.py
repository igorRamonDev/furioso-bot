from data.usuarios import obter_usuarios, salvar_usuario
from services.pandascore_api import obter_jogos_futuros
from datetime import datetime, timedelta
from telegram.ext import Application
import pytz
import json
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("notificacoes")

CAMINHO_AVISOS = "data/avisos_enviados.json"
fuso_brasilia = pytz.timezone("America/Sao_Paulo")

def carregar_avisos_enviados():
    if os.path.exists(CAMINHO_AVISOS):
        with open(CAMINHO_AVISOS, "r") as f:
            conteudo = f.read().strip()
            if conteudo:
                return set(tuple(item) for item in json.loads(conteudo))
    return set()

def salvar_avisos_enviados(avisos):
    os.makedirs(os.path.dirname(CAMINHO_AVISOS), exist_ok=True)
    
    avisos_lista = [list(aviso) for aviso in avisos]
    with open(CAMINHO_AVISOS, "w") as f:
        json.dump(avisos_lista, f)

avisos_enviados = carregar_avisos_enviados()

def adicionar_usuario(chat_id):
    usuarios = obter_usuarios()
    if chat_id not in usuarios:
        usuarios.append(chat_id)
        salvar_usuario(usuarios)
        logger.info(f"Usuário {chat_id} adicionado às notificações")

def remover_usuario(chat_id):
    usuarios = obter_usuarios()
    if chat_id in usuarios:
        usuarios.remove(chat_id)
        salvar_usuario(usuarios)
        logger.info(f"Usuário {chat_id} removido das notificações")

async def verificar_e_enviar_notificacoes(application: Application):
    logger.info("Verificando notificações...")
    jogos = obter_jogos_futuros()
    usuarios = obter_usuarios()
    agora = datetime.now(pytz.utc).astimezone(fuso_brasilia)


    avisos = [
        ("2h", timedelta(hours=2), "⏰ A FURIA joga em 2 horas contra {opponent}!"),
        ("1h", timedelta(hours=1), "⌛ Falta 1 hora para o jogo da FURIA contra {opponent}!"),
        ("30min", timedelta(minutes=30), "⚠️ A FURIA joga em 30 minutos contra {opponent}!"),
        ("inicio", timedelta(seconds=0), "🔥 A FURIA está jogando agora contra {opponent}! Bora torcer! #goFURIA"),
    ]
    
    global avisos_enviados
    avisos_enviados = carregar_avisos_enviados()
    
    logger.info(f"Verificando {len(jogos)} jogos futuros...")
    
    for jogo in jogos:
        if not jogo.get("scheduled_at"):
            logger.info("Jogo sem horário agendado, pulando...")
            continue
            

        opponent = "Adversário desconhecido"
        if jogo.get("opponents") and len(jogo["opponents"]) > 0:
            for team in jogo["opponents"]:
                if team["opponent"]["name"] != "FURIA" and team["opponent"]["id"] != 133063:
                    opponent = team["opponent"]["name"]
                    break
        
        try:
            horario_utc = datetime.fromisoformat(jogo["scheduled_at"].replace("Z", "+00:00"))
            horario_jogo = horario_utc.astimezone(fuso_brasilia)
            delta = horario_jogo - agora
            
            logger.info(f"Jogo contra {opponent} às {horario_jogo.strftime('%H:%M:%S')} (Brasília)")
            logger.info(f"Agora: {agora.strftime('%H:%M:%S')} | Delta: {delta}")
            
            for tag, tempo_aviso, mensagem_template in avisos:
                if abs(delta - tempo_aviso) <= timedelta(minutes=1):
                    chave_aviso = (opponent, tag)
                    
                    if chave_aviso not in avisos_enviados:
                        mensagem = mensagem_template.format(opponent=opponent)
                        logger.info(f"Enviando aviso '{tag}' para jogo contra {opponent}")
                        
                        if not usuarios:
                            logger.warning("Nenhum usuário para notificar")
                            continue
                            
                        for user_id in usuarios:
                            try:
                                # await msg de forma assincrona
                                await application.bot.send_message(chat_id=user_id, text=mensagem)
                                logger.info(f"Notificação enviada para o usuário {user_id}")
                            except Exception as e:
                                logger.error(f"Erro ao enviar notificação para {user_id}: {e}")
                        
                        avisos_enviados.add(chave_aviso)
                        salvar_avisos_enviados(avisos_enviados)
                    else:
                        logger.info(f"Aviso '{tag}' para {opponent} já enviado anteriormente")
        except Exception as e:
            logger.error(f"Erro ao processar jogo: {e}")