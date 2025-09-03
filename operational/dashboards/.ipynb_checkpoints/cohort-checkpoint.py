# operational/dashboards/cohort.py
import streamlit as st
import pandas as pd
from operational.utils.google_sheets import get_sheet_data

def run():
    st.subheader("📊 Dashboard de Coorte")
    
    SPREADSHEET_ID = '15k4L7Sib0ZRTWfeo_wgR5F4YLGQkGEiPZPSPFjwZHHw'
    df = get_sheet_data(SPREADSHEET_ID, 'Sheet1!A1:G100')
    
    if df.empty:
        st.warning("Nenhum dado encontrado na aba 'Sheet1'.")
    else:
        st.dataframe(df)
        st.metric("Total de Usuários", len(df))