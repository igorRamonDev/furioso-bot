import json

# obter lista de users que ativaram
def obter_usuarios():
    try:
        with open('usuarios_notificacoes.json', 'r') as file:
            usuarios = json.load(file)
    except FileNotFoundError:
        usuarios = []
    return usuarios

#salva o chat id de quem ativou
def salvar_usuario(chat_id):
    usuarios = obter_usuarios()
    if chat_id not in usuarios:
        usuarios.append(chat_id)
        with open('usuarios_notificacoes.json', 'w') as file:
            json.dump(usuarios, file)

# remove o chat id de quem desativou
def remover_usuario(chat_id):
    usuarios = obter_usuarios()
    if chat_id in usuarios:
        usuarios.remove(chat_id)
        with open('usuarios_notificacoes.json', 'w') as file:
            json.dump(usuarios, file)

def adicionar_usuario(chat_id):
    salvar_usuario(chat_id)
