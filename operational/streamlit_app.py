# operational/streamlit_app.py
import streamlit as st
import sys
from pathlib import Path

# Adiciona a raiz do projeto ao caminho do Python
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configuração da página (deve vir antes de qualquer output)
st.set_page_config(
    page_title="🎮 Game Product Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🎮 Game Product Management Dashboard")
st.markdown("---")

# Sidebar
st.sidebar.title("📊 Dashboards")
st.sidebar.markdown("Escolha um painel abaixo:")

# Menu de navegação
dashboard = st.sidebar.radio(
    "Selecione o Dashboard:",
    ["🏠 Home", "📈 Análise de Coorte", "💰 Monetização"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Status da Conexão:**")

# Testa conexão com Google Sheets
try:
    from operational.utils.google_sheets import test_connection
    if test_connection():
        st.sidebar.success("✅ Google Sheets OK")
    else:
        st.sidebar.error("❌ Google Sheets Erro")
except Exception as e:
    st.sidebar.error(f"❌ Erro: {e}")

# Roteamento dos dashboards
if dashboard == "🏠 Home":
    st.header("Bem-vindo ao Dashboard de Product Management!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Análise de Coorte")
        st.write("Analise a retenção de usuários ao longo do tempo")
        
    with col2:
        st.subheader("💰 Monetização")
        st.write("Acompanhe métricas de receita e conversão")
    
    st.markdown("---")
    st.info("👈 Use o menu lateral para navegar entre os dashboards")

elif dashboard == "📈 Análise de Coorte":
    try:
        from operational.dashboards.cohort import run as cohort_run
        cohort_run()
    except Exception as e:
        st.error(f"Erro ao carregar dashboard de coorte: {e}")

elif dashboard == "💰 Monetização":
    try:
        from operational.dashboards.monetization import run as monetization_run
        monetization_run()
    except Exception as e:
        st.error(f"Erro ao carregar dashboard de monetização: {e}")

# Footer
st.markdown("---")
st.markdown("*Dashboard desenvolvido para estudos de Python + Streamlit*")