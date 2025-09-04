# operational/components/metrics.py
import streamlit as st
from typing import Dict, Any

def display_kpi_row(metrics: Dict[str, Any], cols: int = 4):
    """Exibe linha de KPIs padronizada"""
    cols_list = st.columns(cols)
    
    for i, (key, data) in enumerate(metrics.items()):
        with cols_list[i % cols]:
            st.metric(
                label=data.get('label', key),
                value=data.get('value', 0),
                delta=data.get('delta'),
                delta_color=data.get('delta_color', 'normal')
            )

def display_data_quality_check(df):
    """Exibe verificação de qualidade dos dados"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Total de Linhas", len(df))
    with col2:
        st.metric("📋 Colunas", len(df.columns))
    with col3:
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
        st.metric("❓ Dados Faltando", f"{missing_pct:.1f}%")