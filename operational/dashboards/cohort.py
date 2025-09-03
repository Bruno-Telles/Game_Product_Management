# operational/dashboards/cohort.py
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Carrega credenciais do Secrets
credentials_json = st.secrets["google_sheets"]["credentials_json"]
creds = service_account.Credentials.from_service_account_info(
    credentials_json,
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)
service = build('sheets', 'v4', credentials=creds)

df = get_sheet_data(service, 'Cohort!A1:G100')