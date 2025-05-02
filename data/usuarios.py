import json

def obter_usuarios():
    try:
        with open('data/usuarios.json', 'r') as f:
            usuarios = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        usuarios = []
    return usuarios

def salvar_usuario(usuarios):
    with open('data/usuarios.json', 'w') as f:
        json.dump(usuarios, f)
