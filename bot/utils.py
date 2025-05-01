import requests
from auth import PANDA_API_TOKEN
from datetime import datetime
import pytz

def obter_jogos_furia_upcoming():
    url = "https://api.pandascore.co/csgo/matches/upcoming"
    headers = {"Authorization": f"Bearer {PANDA_API_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    jogos = response.json()
    brt_timezone = pytz.timezone("America/Sao_Paulo")
    lista = []

    for jogo in jogos:
        try:
            if len(jogo.get('opponents', [])) < 2:
                continue

            time_1 = jogo['opponents'][0]['opponent']['name']
            time_2 = jogo['opponents'][1]['opponent']['name']

            if "FURIA" not in time_1.upper() and "FURIA" not in time_2.upper():
                continue

            data_utc = datetime.strptime(jogo['scheduled_at'], "%Y-%m-%dT%H:%M:%SZ")
            data_utc = pytz.utc.localize(data_utc)
            data_brt = data_utc.astimezone(brt_timezone)

            lista.append({
                'id': jogo['id'],
                'time_1': time_1,
                'time_2': time_2,
                'data': data_brt,
                'campeonato': jogo.get('league', {}).get('name', 'Desconhecido'),
                'nome_jogo': jogo['videogame']['name'],
                'onde_assistir': next((s.get('raw_url') for s in jogo.get('streams_list', []) if s.get('main')), None),
                'nome_completo': jogo.get('name', '')
            })
        except:
            continue

    return lista


def buscar_proximos_jogos():
    jogos = obter_jogos_furia_upcoming()
    if not jogos:
        return "Nenhum jogo da FURIA encontrado para os próximos dias."

    jogos_info = []
    for jogo in jogos:
        jogo_info = (
            f"🎮 Jogo: {jogo['nome_jogo']}\n"
            f"🏆 Campeonato: {jogo['campeonato']} ({jogo['nome_completo'].split(':')[0]})\n"
            f"🔫 {jogo['time_1']} vs {jogo['time_2']}\n"
            f"📅 Data: {jogo['data'].strftime('%d/%m/%Y %H:%M:%S')}\n"
        )
        if jogo['onde_assistir']:
            jogo_info += f"📺 Onde assistir: {jogo['onde_assistir']}\n"
        jogos_info.append(jogo_info)

    return '\n'.join(jogos_info)


def buscar_ultimos_resultados():
    url = "https://api.pandascore.co/csgo/matches/past"
    headers = {"Authorization": f"Bearer {PANDA_API_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return "Erro ao fazer a requisição à API"

    jogos = response.json()

    if not jogos:
        return "Nenhum resultado encontrado"

    resultados_info = []
    brt_timezone = pytz.timezone("America/Sao_Paulo")

    for jogo in jogos:
        try:
            if len(jogo.get('opponents', [])) < 2:
                continue

            time_1 = jogo['opponents'][0]['opponent']['name']
            time_2 = jogo['opponents'][1]['opponent']['name']
            data = jogo['begin_at']
            nome_jogo = jogo['videogame']['name']
            vencedor_id = jogo.get('winner_id')

            if "FURIA" not in time_1.upper() and "FURIA" not in time_2.upper():
                continue

            vencedor = None
            if vencedor_id:
                if jogo['opponents'][0]['opponent']['id'] == vencedor_id:
                    vencedor = time_1
                elif jogo['opponents'][1]['opponent']['id'] == vencedor_id:
                    vencedor = time_2

            campeonato = jogo.get('league', {}).get('name', 'Campeonato desconhecido')
            lower_bracket = jogo.get('name', '').split(":")[0]

            resultados = jogo.get('results', [])
            resultado_1 = resultados[0]['score'] if len(resultados) > 0 else 'N/A'
            resultado_2 = resultados[1]['score'] if len(resultados) > 1 else 'N/A'

            data_utc = datetime.strptime(data, "%Y-%m-%dT%H:%M:%SZ")
            data_utc = pytz.utc.localize(data_utc)
            data_brt = data_utc.astimezone(brt_timezone)

            data_formatada = data_brt.strftime("%d/%m/%Y %H:%M:%S")

            resultado_info = f"🎮 Jogo: {nome_jogo}\n"
            resultado_info += f"🏆 Campeonato: {campeonato} ({lower_bracket})\n"
            resultado_info += f"🔫 {time_1} {resultado_1} x {resultado_2} {time_2}\n"
            resultado_info += f"📅 Data: {data_formatada}\n"

            if vencedor:
                resultado_info += f"🏆 Vencedor: {vencedor}\n"

            resultados_info.append(resultado_info)

            if len(resultados_info) >= 5:
                break

        except Exception as e:
            print(f"Erro ao processar o jogo: {e}")
            continue

    if resultados_info:
        resultado = '\n'.join(resultados_info)
    else:
        resultado = "Nenhum resultado recente da FURIA encontrado."

    return resultado
