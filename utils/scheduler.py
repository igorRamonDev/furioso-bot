from apscheduler.schedulers.background import BackgroundScheduler
from telegram.ext import Application
from services.notificacoes import verificar_e_enviar_notificacoes

def iniciar_scheduler(application: Application):
    scheduler = BackgroundScheduler()
    scheduler.add_job(verificar_e_enviar_notificacoes, 'interval', minutes=1, args=[application])
    scheduler.start()
