# operational/utils/google_sheets.py
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_google_sheets_client():
    # Cria e retorna um cliente do Google Sheets usando st.secrets
    try:
        credentials_json = st.secrets["google_sheets"]["credentials_json"]
        creds = service_account.Credentials.from_service_account_info(
            credentials_json,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        return build('sheets', 'v4', credentials=creds)
    except Exception as e:
        st.error(f"❌ Erro ao conectar ao Google Sheets: {e}")
        return None

def get_sheet_data(spreadsheet_id, range_name='Sheet1!A1:Z1000'):
    # Carrega dados de uma planilha como DataFrame
    service = get_google_sheets_client()
    if not service:
        return pd.DataFrame()

    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        values = result.get('values', [])
        if not values:
            return pd.DataFrame()
        return pd.DataFrame(values[1:], columns=values[0])
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return pd.DataFrame()