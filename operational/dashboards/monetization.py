# operational/dashboards/monetization.py
import streamlit as st
import pandas as pd
from operational.utils import get_sheet_data

def run():
    st.subheader("💰 Monetização")
    SPREADSHEET_ID = '15k4L7Sib0ZRTWfeo_wgR5F4YLGQkGEiPZPSPFjwZHHw'
    df = get_sheet_data(SPREADSHEET_ID, 'Monetization!A1:F50')

    if df.empty:
        st.warning("Nenhum dado encontrado na aba 'Monetization'.")
    else:
        st.dataframe(df, use_container_width=True)
        st.metric("Receita Total", f"R$ {df['Revenue'].sum():,.2f}")