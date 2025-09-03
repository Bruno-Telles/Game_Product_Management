# operational/streamlit_app.py
import streamlit as st
import os
import sys
from pathlib import Path

# Adiciona a raiz do projeto ao caminho do Python
sys.path.append(str(Path(__file__).parent.parent / 'operational'))

# Configuração da página (deve vir antes de qualquer output)
st.set_page_config(page_title="🎮 Game Product Dashboard", layout="wide")
st.sidebar.title("📊 Dashboards")
st.sidebar.markdown("Escolha um painel abaixo:")

# Menu de navegação
dashboard = st.sidebar.radio(
    "Dashboard",
    ["Análise de Coorte", "Monetização"]
)

# === Funções de Conexão com Google Sheets ===
def get_google_sheets_client():
    """Cria e retorna um cliente do Google Sheets usando st.secrets."""
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
    """Carrega dados de uma planilha como DataFrame."""
    service = get_google_sheets_client()
    if not service:
        return None

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

# === Roteamento dos Dashboards ===
SPREADSHEET_ID = '15k4L7Sib0ZRTWfeo_wgR5F4YLGQkGEiPZPSPFjwZHHw'

if dashboard == "Análise de Coorte":
    st.title('📅 Cohort Analysis')
    df = get_sheet_data(SPREADSHEET_ID, 'Cohort!A1:G100')
    
    if df is not None and not df.empty:
        st.dataframe(df, use_container_width=True)
        st.metric("Total de Coortes", len(df))
    else:
        st.warning("Nenhum dado encontrado na aba 'Cohort'.")

elif dashboard == "Monetização":
    st.title("💰 Monetização")
    df = get_sheet_data(SPREADSHEET_ID, 'Monetization!A1:F50')
    
    if df is not None and not df.empty:
        st.dataframe(df, use_container_width=True)
        st.metric("Receita Total", f"R$ {df['Revenue'].sum():,.2f}")
    else:
        st.warning("Nenhum dado encontrado na aba 'Monetization'.")