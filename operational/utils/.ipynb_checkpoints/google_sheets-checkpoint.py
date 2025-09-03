# operational/utils/google_sheets.py
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from .paths import CREDENTIALS_PATH

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def get_google_sheets_client():
    '''Cria e retorna um cliente do Google Sheets.'''
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH, scopes=SCOPES
    )
    return build('sheets', 'v4', credentials=creds)

def get_sheet_data(spreadsheet_id, range_name='Sheet1!A1:Z1000'):
    '''Carrega dados de uma planilha como DataFrame.'''
    service = get_google_sheets_client()
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()
    
    values = result.get('values', [])
    if not values:
        return pd.DataFrame()
    
    df = pd.DataFrame(values[1:], columns=values[0])
    return df