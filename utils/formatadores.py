from datetime import datetime
import pytz
from services.pandascore_api import obter_jogos_futuros, obter_resultados_passados

BRASILIA_TZ = pytz.timezone('America/Sao_Paulo')

def buscar_proximos_jogos():
    jogos = obter_jogos_futuros()
    if not jogos:
        return "🔥 Por enquanto, o servidor tá tranquilo... Nenhuma partida marcada. Mas a FURIA nunca dorme."
    return "\n\n".join([formatar_jogo(jogo) for jogo in jogos])

def buscar_ultimos_resultados():
    resultados = obter_resultados_passados()
    if not resultados:
        return "🕶️ Sem registros anteriores... ou destruímos tanto que nem sobrou rastro!"
    return "\n\n".join([formatar_resultado(resultado) for resultado in resultados])

def formatar_data_horario_brasilia(data_utc):
    if not data_utc:
        return "Data indefinida"
    try:
        dt_utc = datetime.fromisoformat(data_utc.replace("Z", "+00:00"))
        dt_brasilia = dt_utc.astimezone(BRASILIA_TZ)
        return dt_brasilia.strftime("%d/%m/%Y %H:%M:%S")
    except Exception as e:
        print(f"Erro ao formatar data: {e}")
        return "Data inválida"

def formatar_jogo(jogo):
    try:
        oponentes = jogo["opponents"]
        
        team1 = oponentes[0]["opponent"]["name"] if len(oponentes) > 0 else "Time 1"
        team2 = oponentes[1]["opponent"]["name"] if len(oponentes) > 1 else "Time 2"
        
        campeonato = jogo.get("league", {}).get("name", "Campeonato não especificado")
        fase = jogo.get("tournament", {}).get("name", "Fase não especificada")
        semifinal = jogo.get("name", "")

        videogame = jogo.get("videogame_title", {}).get("name", "CS2")
        
        horario_jogo_utc = jogo.get("begin_at", "")
        horario_jogo_brasilia = formatar_data_horario_brasilia(horario_jogo_utc)
        
        transmissao = "Transmissão não disponível."
        streams = jogo.get("streams_list", [])
        if streams:
            for stream in streams:
                if stream.get("main"):
                    transmissao = f"{stream.get('raw_url', 'Link indisponível')}"
                    break
        
        return f"""🎮 {videogame}
🏆 {campeonato}
🏆 {fase} {semifinal}
🔫 {team1} vs {team2}
📅 {horario_jogo_brasilia}
📺 {transmissao}"""

    except Exception as e:
        print(f"Erro ao formatar jogo: {e}")
        return "Erro ao formatar dados do jogo."

def formatar_resultado(resultado):
    try:
        oponentes = resultado.get("opponents", [])
        
        team1 = oponentes[0]["opponent"]["name"] if len(oponentes) > 0 else "Time 1"
        team2 = oponentes[1]["opponent"]["name"] if len(oponentes) > 1 else "Time 2"
        
        campeonato = resultado.get("league", {}).get("name", "Campeonato não especificado")
        fase = resultado.get("tournament", {}).get("name", "Fase não especificada")
        semifinal = resultado.get("name", "")
        
        videogame = resultado.get("videogame_title", {}).get("name", "CS2")
        
        horario_jogo_utc = resultado.get("begin_at", "")
        horario_jogo_brasilia = formatar_data_horario_brasilia(horario_jogo_utc)
 
        score_team1 = "N/A"
        score_team2 = "N/A"
        
        if resultado.get("results"):
            team1_id = oponentes[0]["opponent"]["id"] if len(oponentes) > 0 else None
            team2_id = oponentes[1]["opponent"]["id"] if len(oponentes) > 1 else None
            
            for result in resultado["results"]:
                if result["team_id"] == team1_id:
                    score_team1 = result["score"]
                elif result["team_id"] == team2_id:
                    score_team2 = result["score"]
        
        resultado_final = f"{team1} {score_team1} - {score_team2} {team2}"
        
        return f"""🎮 {videogame}
🏆 {campeonato}
🏆 {fase} {semifinal}
🔫 {team1} vs {team2}
📅 {horario_jogo_brasilia}
📝 {resultado_final}"""

    except Exception as e:
        print(f"Erro ao formatar resultado: {e}")
        return "Erro ao formatar dados do resultado."