# operational/utils/google_sheets.py
import streamlit as st
import json
import os
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd

def get_google_sheets_client():
    """Cria e retorna um cliente do Google Sheets."""
    try:
        # Primeiro tenta usar st.secrets (para Streamlit Cloud)
        if hasattr(st, 'secrets') and 'google_sheets' in st.secrets:
            credentials_json = st.secrets["google_sheets"]["credentials_json"]
            if isinstance(credentials_json, str):
                credentials_json = json.loads(credentials_json)
        else:
            # Fallback para arquivo local
            config_path = Path(__file__).parent.parent.parent / "config" / "credentials.json"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    credentials_json = json.load(f)
            else:
                st.error("❌ Arquivo credentials.json não encontrado!")
                return None
        
        creds = service_account.Credentials.from_service_account_info(
            credentials_json,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        return build('sheets', 'v4', credentials=creds)
        
    except Exception as e:
        st.error(f"❌ Erro ao conectar ao Google Sheets: {e}")
        st.error("Verifique se o arquivo credentials.json está configurado corretamente.")
        return None

def get_sheet_data(spreadsheet_id, sheet_name='Sheet1', range_cells='A1:Z1000'):
    """Carrega dados de uma planilha como DataFrame."""
    service = get_google_sheets_client()
    if not service:
        return pd.DataFrame()

    try:
        # Constrói o range completo
        range_name = f"{sheet_name}!{range_cells}"
        
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        
        values = result.get('values', [])
        if not values:
            st.warning(f"⚠️ Nenhum dado encontrado na aba '{sheet_name}'")
            return pd.DataFrame()
            
        # Se só tem uma linha, não há dados além do cabeçalho
        if len(values) == 1:
            st.warning(f"⚠️ Apenas cabeçalho encontrado na aba '{sheet_name}'")
            return pd.DataFrame(columns=values[0])
            
        # Cria DataFrame com primeira linha como cabeçalho
        df = pd.DataFrame(values[1:], columns=values[0])
        
        # Remove linhas completamente vazias
        df = df.dropna(how='all')
        
        st.success(f"✅ Dados carregados da aba '{sheet_name}': {len(df)} linhas")
        return df
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados da aba '{sheet_name}': {e}")
        return pd.DataFrame()

def test_connection():
    """Testa a conexão com Google Sheets."""
    st.write("🔄 Testando conexão...")
    service = get_google_sheets_client()
    if service:
        st.success("✅ Conexão estabelecida com sucesso!")
        return True
    else:
        st.error("❌ Falha na conexão!")
        return False