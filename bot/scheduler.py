from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from bot.utils import obter_jogos_furia_upcoming
from bot.notificacoes import obter_usuarios
import pytz

def iniciar_scheduler(application):
    scheduler = BackgroundScheduler(timezone='America/Sao_Paulo')

    def enviar_alerta(application, mensagem):
        for chat_id in obter_usuarios():
            application.create_task(
                application.bot.send_message(chat_id=chat_id, text=mensagem)
            )

    def checar_jogos_e_agendar():
        jogos = obter_jogos_furia_upcoming()
        agora = datetime.now(pytz.timezone("America/Sao_Paulo"))

        for jogo in jogos:
            jogo_id = jogo["id"]
            data = jogo["data"]
            time_1 = jogo["time_1"]
            time_2 = jogo["time_2"]
            campeonato = jogo["campeonato"]
            onde_assistir = jogo["onde_assistir"]

            mensagem_base = (
                f"🏆 {campeonato}\n"
                f"🔫 {time_1} vs {time_2}\n"
                f"📅 {data.strftime('%d/%m/%Y %H:%M:%S')}\n"
            )
            if onde_assistir:
                mensagem_base += f"📺 Onde assistir: {onde_assistir}"

            horario_30min = data - timedelta(minutes=30)
            if horario_30min > agora:
                scheduler.add_job(
                    enviar_alerta,
                    trigger="date",
                    run_date=horario_30min,
                    args=[application, f"⏰ Faltam 30 minutos para o jogo da FURIA!\n\n{mensagem_base}"],
                    id=f"{jogo_id}_30min",
                    replace_existing=True
                )

            if data > agora:
                scheduler.add_job(
                    enviar_alerta,
                    trigger="date",
                    run_date=data,
                    args=[application, f"🔥 Começou o jogo da FURIA!\n\n{mensagem_base}"],
                    id=f"{jogo_id}_inicio",
                    replace_existing=True
                )

    checar_jogos_e_agendar()
    scheduler.add_job(checar_jogos_e_agendar, 'interval', hours=1)
    scheduler.start()