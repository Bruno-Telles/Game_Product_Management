# operational/dashboards/monetization.py
import streamlit as st
import pandas as pd
import numpy as np
from operational.utils.google_sheets import get_sheet_data

# ID da sua planilha (extraído da URL)
SPREADSHEET_ID = "15k4L7Sib0ZRTWfeo_wgR5F4YLGQkGEiPZPSPFjwZHHw"

def run():
    """Dashboard de Monetização"""
    st.header("💰 Dashboard de Monetização")
    st.markdown("Análise de receita, conversão e métricas financeiras")
    
    # Botão para recarregar dados
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔄 Recarregar Dados"):
            st.cache_data.clear()
    
    # Carrega dados da planilha
    with st.spinner("Carregando dados da planilha..."):
        df = load_monetization_data()
    
    if df.empty:
        st.warning("⚠️ Não foi possível carregar os dados. Verifique:")
        st.markdown("""
        - Se a planilha existe e tem dados na aba 'Monetization'
        - Se as credenciais do Google Sheets estão corretas
        - Se a planilha está compartilhada com o email de serviço
        """)
        
        # Mostra dados de exemplo
        st.subheader("📊 Exemplo de Dados de Monetização")
        show_sample_data()
        return
    
    # Mostra os dados carregados
    st.subheader("📊 Dados Carregados")
    st.dataframe(df, use_container_width=True)
    
    # Métricas básicas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Linhas", len(df))
    with col2:
        st.metric("Colunas", len(df.columns))
    with col3:
        if not df.empty:
            st.metric("Primeira Data", df.iloc[0, 0] if len(df.columns) > 0 else "N/A")

@st.cache_data(ttl=300)  # Cache por 5 minutos
def load_monetization_data():
    """Carrega dados de monetização da planilha"""
    return get_sheet_data(
        spreadsheet_id=SPREADSHEET_ID,
        sheet_name="Monetization",
        range_cells="A1:Z100"
    )

def show_sample_data():
    """Mostra dados de exemplo para teste"""
    # Dados de exemplo
    sample_data = {
        'Data': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'Receita': [15000, 18000, 16500],
        'DAU': [5000, 5200, 4900],
        'ARPU': [3.0, 3.46, 3.37],
        'Conversão': [0.05, 0.052, 0.048]
    }
    
    df_sample = pd.DataFrame(sample_data)
    st.dataframe(df_sample, use_container_width=True)
    
    st.info("💡 Estes são dados de exemplo. Configure sua planilha com estrutura similar.")

if __name__ == "__main__":
    run()