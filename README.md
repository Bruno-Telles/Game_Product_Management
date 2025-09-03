# GAME PRODUCT MANAGEMENT
Dashboard para análise de jogos diretamente do Google Sheets e/ou Faker.

## Como usar

    1. Crie um arquivo 'credentials.json' (veja instruções abaixo)
    2. Coloque no 'config/'
    3. Altere o 'sheet_id' no 'streamlit_app.py'
    4. Rode: 'streamlit run streamlit_app.py'

## Como gerar credentials.json

    1. Acesse: https://console.cloud.google.com/
    2. Crie um projeto
    3. Ative a API do Google Sheets
    4. Crie uma conta de serviço
    5. Baixe o JSON e renomeie para 'credentials.json'

    Mais detalhes: https://gspread.readthedocs.io/en/latest/
