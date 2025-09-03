# streamlit_app.py
'''
Dashboard Interativo para Product Manager
Conecta ao Google Sheets e mostra métricas em tempo real
'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="🎮 Game Product Management", layout="wide")
st.title("🎮 Metrics and Strategic Analysis")
st.markdown("Dados atualizados diretamente do **Google Sheets**")

# Carregar dados (com cache para não recarregar sempre)
@st.cache_data(ttl=300)  # Atualiza a cada 5 minutos
def load_data():
    from utils.google_sheets import connect_to_sheet
    # 🔽 Substitua com seus dados:
    credentials_path = "config/credentials.json"  # Arquivo que você vai baixar
    sheet_id = "15k4L7Sib0ZRTWfeo_wgR5F4YLGQkGEiPZPSPFjwZHHw"  # Pegue do URL do Sheet
    return connect_to_sheet(credentials_path, sheet_id, "Dados")

# Tentar carregar dados
try:
    df = load_data()
    st.success("✅ Dados carregados com sucesso!")
    
    # Mostrar amostra
    st.subheader("Prévia dos Dados")
    st.dataframe(df.head())

    
    '''# Abas
    tab1, tab2, tab3 = st.tabs(["📈 Retenção", "💰 Monetização", "🧪 A/B Test"])

    with tab1:
        st.subheader("Cohort Retention")
        from dashboards.cohort import analyze_cohort, plot_retention
        retention = analyze_cohort(df)
        st.write(retention)
        fig = plot_retention(retention)
        st.pyplot(fig)

    with tab2:
        st.subheader("Monetização")
        from dashboards.monetization import analyze_monetization, plot_revenue
        monetization = analyze_monetization(df)
        st.write(monetization)
        fig = plot_revenue(df)
        st.pyplot(fig)

    with tab3:
        st.subheader("A/B Test")
        if 'group' in df.columns and 'converted' in df.columns:
            from dashboards.ab_test import analyze_ab_test, plot_ab_results
            ab_results = analyze_ab_test(df)
            st.write(ab_results)
            fig = plot_ab_results(ab_results['contingency'])
            st.pyplot(fig)
        else:
            st.warning("Adicione colunas 'group' e 'converted' no Sheet para A/B test.")
'''
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    st.info("Verifique: credentials.json, sheet_id, e conexão com internet.")