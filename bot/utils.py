import requests
from auth import PANDA_API_TOKEN
from datetime import datetime
import pytz

def buscar_proximos_jogos():
    url = "https://api.pandascore.co/csgo/matches/upcoming"
    headers = {"Authorization": f"Bearer {PANDA_API_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return "Erro ao fazer a requisição à API"

    jogos = response.json()

    if not jogos:
        return "Nenhum jogo encontrado"

    jogos_info = []

    # ajuste horario
    brt_timezone = pytz.timezone("America/Sao_Paulo")

    for jogo in jogos:
        try:
            if len(jogo.get('opponents', [])) < 2:
                continue

            time_1 = jogo['opponents'][0]['opponent']['name']
            time_2 = jogo['opponents'][1]['opponent']['name']
            data = jogo['scheduled_at']
            nome_jogo = jogo['videogame_title']['name']  # Pegando o nome do jogo (Counter-Strike 2)

            # Filtrar se "FURIA" esta entre os times
            if "FURIA" not in (time_1.upper(), time_2.upper()):
                continue  # se n tiver "FURIA" pula
 
            # obtendo info do campeonato e fase
            campeonato = jogo.get('league', {}).get('name', 'Campeonato desconhecido')
            lower_bracket = jogo.get('name', '').split(":")[0]

            #live
            streams = jogo.get('streams_list', [])
            onde_assistir = None
            if streams:
                for stream in streams:
                    if stream.get('main', False):
                        onde_assistir = stream.get('raw_url', None)
                        break

            # converte data
            data_utc = datetime.strptime(data, "%Y-%m-%dT%H:%M:%SZ")
            data_utc = pytz.utc.localize(data_utc)  # localiza o horário UTC
            data_brt = data_utc.astimezone(brt_timezone)  # converte para horário de Brasília

            # formata data
            data_formatada = data_brt.strftime("%d/%m/%Y %H:%M:%S") 

            #formata info da partida
            jogo_info = f"🎮 Jogo: {nome_jogo}\n"
            jogo_info += f"🏆 Campeonato: {campeonato} ({lower_bracket})\n"
            jogo_info += f"🔫 {time_1} vs {time_2}\n"
            jogo_info += f"📅 Data: {data_formatada}\n"

            if onde_assistir:
                jogo_info += f"📺 Onde assistir: {onde_assistir}\n"
            
            jogos_info.append(jogo_info)

        except KeyError:
            continue

    if jogos_info:
        resultado = '\n'.join(jogos_info)
    else:
        resultado = "Nenhum jogo da FURIA encontrado para os proximos dias."

    print(resultado)
    return resultado
