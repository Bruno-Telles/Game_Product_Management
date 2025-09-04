# operational/dashboards/cohort.py
import streamlit as st
import pandas as pd
from operational.utils import get_sheet_data

"""from google.oauth2 import service_account
from googleapiclient.discovery import build"""

def run():
    st.subheader("📅 Análise de Coorte")
    SPREADSHEET_ID = '15k4L7Sib0ZRTWfeo_wgR5F4YLGQkGEiPZPSPFjwZHHw'
    df = get_sheet_data(SPREADSHEET_ID, 'Cohort!A1:G100')

    if df.empty:
        st.warning("Nenhum dado encontrado na aba 'Cohort'.")
    else:
        st.dataframe(df, use_container_width=True)
        st.metric('Total de Coortes', len(df))
