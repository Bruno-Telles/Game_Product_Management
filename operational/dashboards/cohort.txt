# operational/dashboards/cohort.py
import streamlit as st
import pandas as pd
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build

def run():
    st.subheader("📅 Análise de Coorte")

    try:
        # Carrega credenciais do Secrets
        credentials_json = st.secrets["google_sheets"]["credentials_json"]
        creds = service_account.Credentials.from_service_account_info(
            credentials_json,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        service = build('sheets', 'v4', credentials=creds)

        SPREADSHEET_ID = '15k4L7Sib0ZRTWfeo_wgR5F4YLGQkGEiPZPSPFjwZHHw'
        df = get_sheet_data(service, 'Cohort!A1:G100')

        if df.empty:
            st.warning("Nenhum dado encontrado na aba 'Cohort'.")
        else:
            st.dataframe(df)
    except Exception as e:
        st.error(f"Erro ao conectar ao Google Sheets: {e}")


print('Módulos disponíveis:', sys.modules.keys()) 