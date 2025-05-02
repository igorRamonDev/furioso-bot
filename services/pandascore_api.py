import requests
from config.auth import PANDA_API_TOKEN

HEADERS = {"Authorization": f"Bearer {PANDA_API_TOKEN}"}
TEAM_ID = 3246  #TESTE USANDO A HEROIC

def obter_jogos_futuros():
    url = f"https://api.pandascore.co/csgo/matches/upcoming?per_page=20"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Erro na API: {response.status_code}")
        return []

    jogos = response.json()
    resultados = []

    for jogo in jogos:
        if not jogo["opponents"] or not any(op["opponent"]["id"] == TEAM_ID for op in jogo["opponents"]):
            continue

        resultados.append(jogo)

    return resultados

def obter_resultados_passados():
    url = f"https://api.pandascore.co/csgo/matches/past"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Erro na API: {response.status_code}")
        return []

    jogos = response.json()
    resultados = []

    for jogo in jogos:
        if not jogo["opponents"] or not any(op["opponent"]["id"] == TEAM_ID for op in jogo["opponents"]):
            continue

        resultados.append(jogo)

    return resultados
