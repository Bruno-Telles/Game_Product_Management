# operational/streamlit_app.py
import streamlit as st
import sys
import os
from pathlib import Path

# Adiciona operational ao sys.path para conseguir importar os módulos
sys.path.append(str(Path(__file__).parent.parent / 'operational'))

# Adiciona a pasta raiz ao caminho do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa o dashboard de coorte
from operational.dashboards.cohort import run as cohort_dashboard

# Configuração da página
st.set_page_config(page_title="🎮 Game Product Dashboard", layout="wide")
st.sidebar.title("📊 Dashboards")
st.sidebar.markdown("Escolha um painel abaixo:")

# Menu de navegação
dashboard = st.sidebar.radio("Dashboard", ["Análise de Coorte"])


# Roteamento
if dashboard == "Cohort Analysis":
    cohort.run()
'''    
elif dashboard == "Monetization":
    monetization.run()
elif dashboard == "A/B Tests":
    ab_test.run()
'''