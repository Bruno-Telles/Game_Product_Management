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
        # Usa diretamente o arquivo credentials.json local
        config_path = Path(__file__).parent.parent.parent / "Configuração" / "config" / "credentials.json"
        
        if not config_path.exists():
            st.error(f"❌ Arquivo credentials.json não encontrado em: {config_path}")
            return None
            
        with open(config_path, 'r', encoding='utf-8') as f:
            credentials_json = json.load(f)
        
        creds = service_account.Credentials.from_service_account_info(
            credentials_json,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        
        service = build('sheets', 'v4', credentials=creds)
        return service
        
    except FileNotFoundError:
        st.error(f"❌ Arquivo credentials.json não encontrado em: {config_path}")
        return None
    except json.JSONDecodeError:
        st.error("❌ Erro ao decodificar credentials.json. Verifique se o arquivo está em formato JSON válido.")
        return None
    except Exception as e:
        st.error(f"❌ Erro ao conectar ao Google Sheets: {e}")
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