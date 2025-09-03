# test_sheets.py
import gspread
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd

# 1. Pasta do script atual: operational/utils
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Volta duas pastas para chegar na raiz do projeto
project_root = os.path.dirname(os.path.dirname(script_dir))  # volta de utils → operational → raiz

# 3. Monta o caminho para config
CREDENTIALS_PATH = os.path.join(project_root, 'config', 'credentials.json')

# 4. Verifica se o arquivo existe
if not os.path.exists(CREDENTIALS_PATH):
    print("Diretório atual:", os.getcwd())
    print("Caminho calculado:", CREDENTIALS_PATH)
    raise FileNotFoundError(f"Arquivo não encontrado: {CREDENTIALS_PATH}")

# 5. Define os escopos
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# 6. Carrega credenciais
creds = service_account.Credentials.from_service_account_file(
    CREDENTIALS_PATH, scopes=SCOPES
)

# 7. Testa conexão com Sheets (coloque seu ID real)
service = build('sheets', 'v4', credentials=creds)
SPREADSHEET_ID = '15k4L7Sib0ZRTWfeo_wgR5F4YLGQkGEiPZPSPFjwZHHw'  # Substitua pelo ID real
RANGE_NAME = 'Sheet1!A1:F2'  # Ajuste conforme sua estrutura

# 8. Faz a requisição
result = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range=RANGE_NAME
).execute()

values = result.get('values', [])

if not values:
    print("⚠️ Nenhum dado encontrado na planilha.")
else:
    df = pd.DataFrame(values[1:], columns=values[0])
    print("✅ Dados carregados com sucesso!")
    print(df.head())