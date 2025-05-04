from apscheduler.schedulers.background import BackgroundScheduler
from telegram.ext import Application
from services.notificacoes import verificar_e_enviar_notificacoes
import logging
import asyncio

def iniciar_scheduler(application: Application):
    """
    Inicia um scheduler em segundo plano para executar verificações de notificações
    a cada minuto e enviar os alertas para os usuários.
    """
    logging.info("Inicializando scheduler de notificações...")
    
    scheduler = BackgroundScheduler()
    
    def run_async_function(app):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(verificar_e_enviar_notificacoes(app))
        loop.close()
    
    scheduler.add_job(
        run_async_function, 
        'interval', 
        minutes=1, 
        args=[application],
        misfire_grace_time=30 
    )
    
    scheduler.start()
    logging.info("Scheduler de notificações iniciado com sucesso!")