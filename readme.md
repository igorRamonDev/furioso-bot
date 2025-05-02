![Furioso Bot](assets/imgs/FURIOSO-BOT.png)

# 🦍 FURIOSO BOT

Bot do Telegram para acompanhar **próximos jogos** e **resultados recentes** da equipe de CS2 **FURIA**!

---

## 🚀 Como rodar

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/furioso-bot.git
    cd furioso-bot
    ```

2. Crie e ative um ambiente virtual:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux / Mac
    venv\Scripts\activate     # Windows
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure o arquivo `auth.py`:

    Crie uma pasta `config` com um arquivo chamado `auth.py` e adicione seu token do Telegram e token da API Pandascore:

    ```python
    # auth.py
    TOKEN = 'SEU_TOKEN_DO_TELEGRAM'
    PANDA_API_TOKEN = 'SEU_TOKEN_DA_API_PANDASCORE'
    ```

5. Rode o bot:

    ```bash
    python3 main.py
    ```

---

## 🛠 Tecnologias usadas

- [Python 3.12](https://www.python.org/)
- [python-telegram-bot](https://python-telegram-bot.org/)
- [Pandascore API](https://developers.pandascore.co/)
- [APScheduler](https://apscheduler.readthedocs.io/)
- [Requests](https://requests.readthedocs.io/)

---

## 🎯 Funcionalidades

- **Botões interativos** no Telegram para navegar pelo bot.
- Buscar **próximos jogos** da FURIA.
- Exibir **resultados recentes** da FURIA.
- Enviar **notificações** para usuários sobre jogos da FURIA, como alertas 30 minutos antes e no início das partidas.
- **Integração com a API oficial de eSports** da Pandascore.

---

## 📷 Screenshots

> Quando o usuário digitar `/start`:

- Opções aparecem como botões:
  - 🎯 Próximos Jogos da FURIA
  - 🏆 Resultados Recentes
  - 📖 Nossa história
  - 🎯 Line-up da FURIA
  - 🔔 Ativar/Desativar notificações

---

Feito com ❤️ por **igorRamonDev**.
