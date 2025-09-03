'''
Módulo para ler dados do Google Sheets
'''

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def connect_to_sheet(credentials_path, sheet_id, worksheet_name="Sheet1"):
    '''
    Conecta ao Google e retorna um DataFrame.

    Args:
        credentials_path (str): Caminho para o arquivo credentials.json
        sheet_id (str): ID da planilha (parte do URL)
        worksheet_name (str): Nome da aba (ex: "Dados", "Sheet1")

    Returns:
        pd.DataFrame: Dados da planilha
    '''

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(sheet_id).worksheet(worksheet_name)
    data = sheet.get_all_records()
    return pd.DataFrame(data)

print('test')