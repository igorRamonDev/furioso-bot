import json
import os
import logging

logger = logging.getLogger("usuarios")

ARQUIVO_USUARIOS = 'data/usuarios.json'

def obter_usuarios():
    try:
        with open(ARQUIVO_USUARIOS, 'r') as f:
            usuarios = json.load(f)
        return usuarios
    except FileNotFoundError:
        logger.info(f"Arquivo {ARQUIVO_USUARIOS} não encontrado. Criando nova lista.")
        return []
    except json.JSONDecodeError:
        logger.warning(f"Erro ao decodificar {ARQUIVO_USUARIOS}. O arquivo pode estar vazio ou malformado.")
        return []
    except Exception as e:
        logger.error(f"Erro ao carregar usuários: {e}")
        return []

def salvar_usuario(usuarios):
    try:
        os.makedirs(os.path.dirname(ARQUIVO_USUARIOS), exist_ok=True)
        
        with open(ARQUIVO_USUARIOS, 'w') as f:
            json.dump(usuarios, f)
        logger.info(f"Lista de usuários atualizada. Total: {len(usuarios)}")
    except Exception as e:
        logger.error(f"Erro ao salvar usuários: {e}")