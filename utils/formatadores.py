from datetime import datetime
from services.pandascore_api import obter_jogos_futuros, obter_resultados_passados

def buscar_proximos_jogos():
    jogos = obter_jogos_futuros()
    if not jogos:
        return "Nenhuma partida futura encontrada."

    return "\n".join([formatar_jogo(jogo) for jogo in jogos])

def buscar_ultimos_resultados():
    resultados = obter_resultados_passados()
    if not resultados:
        return "Nenhum resultado passado encontrado."

    return "\n".join([formatar_resultado(resultado) for resultado in resultados])

from datetime import datetime

from datetime import datetime
import pytz

BRASILIA_TZ = pytz.timezone('America/Sao_Paulo')

def formatar_jogo(jogo):
    """
    Formata os dados do jogo para exibição, no formato requerido.
    """
    oponentes = jogo["opponents"]
    team1 = oponentes[0]["opponent"]["name"]
    team2 = oponentes[1]["opponent"]["name"]
    campeonato = jogo["league"]["name"]
    fase = jogo["tournament"]["name"] 
    semifinal = jogo["name"] 
    videogame = jogo["videogame_title"]["name"] 
    horario_jogo_utc = jogo["begin_at"]
    horario_jogo_utc = datetime.fromisoformat(horario_jogo_utc.replace("Z", "+00:00"))
    
    horario_jogo_brasilia = horario_jogo_utc.astimezone(BRASILIA_TZ).strftime("%d/%m/%Y %H:%M:%S")

    streams = jogo.get("streams_list", [])
    transmissao = "Transmissão não disponível."
    if streams:
        for stream in streams:
            if stream.get("main"):
                transmissao = f"{stream['raw_url']}"
                break

    return f"""🎮 {videogame} 
🏆 {campeonato}
🏆 {fase} {semifinal}
🔫 {team1} vs {team2}
📅 {horario_jogo_brasilia}
📺 {transmissao}"""

def formatar_data_horario_brasilia(data_utc):
    from datetime import datetime
    import pytz

    if not data_utc:
        return "Data indefinida"
    dt_utc = datetime.fromisoformat(data_utc.replace("Z", "+00:00"))
    brasilia = pytz.timezone("America/Sao_Paulo")
    dt_brasilia = dt_utc.astimezone(brasilia)
    return dt_brasilia.strftime("%d/%m/%Y %H:%M:%S")

def formatar_resultado(resultado):
    """
    Formata os dados de um resultado de jogo para exibição, no formato requerido.
    """
    oponentes = resultado["opponents"]
    team1 = oponentes[0]["opponent"]["name"]
    team2 = oponentes[1]["opponent"]["name"]
    campeonato = resultado["league"]["name"]
    fase = resultado["tournament"]["name"]  
    semifinal = resultado["name"] 
    videogame = resultado["videogame_title"]["name"]  
    horario_jogo_utc = resultado["begin_at"]
    horario_jogo_utc = datetime.fromisoformat(horario_jogo_utc.replace("Z", "+00:00"))

    horario_jogo_brasilia = horario_jogo_utc.astimezone(BRASILIA_TZ).strftime("%d/%m/%Y %H:%M:%S")

    score_team1 = "N/A"
    score_team2 = "N/A"
    
    if resultado.get("results"):
        for result in resultado["results"]:
            if result["team_id"] == oponentes[0]["opponent"]["id"]:
                score_team1 = result["score"]
            elif result["team_id"] == oponentes[1]["opponent"]["id"]:
                score_team2 = result["score"]

    resultado_final = f"{team1} {score_team1} - {score_team2} {team2}"

    return f"""🎮 {videogame} 
🏆 {campeonato}
🏆 {fase} {semifinal}
🔫 {team1} vs {team2}
📅 {horario_jogo_brasilia}
📝 {resultado_final}"""


