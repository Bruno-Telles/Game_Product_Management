# operational/utils/google_sheets_client.py
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import Optional, List
import logging
from config.settings import settings

class GoogleSheetsClient:
    def __init__(self):
        self._service = None
        self.logger = logging.getLogger(__name__)
    
    @property
    def service(self):
        """Lazy loading do serviço Google Sheets"""
        if self._service is None:
            self._service = self._create_service()
        return self._service
    
    def _create_service(self):
        """Cria o serviço Google Sheets"""
        try:
            credentials_info = settings.get_google_credentials()
            creds = service_account.Credentials.from_service_account_info(
                credentials_info,
                scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
            )
            return build('sheets', 'v4', credentials=creds)
        except Exception as e:
            self.logger.error(f"Erro ao criar serviço Google Sheets: {e}")
            raise
    
    @st.cache_data(ttl=settings.cache_ttl if hasattr(settings, 'cache_ttl') else 300)
    def get_sheet_data(self, sheet_name: str, range_cells: str = "A1:Z1000") -> pd.DataFrame:
        """Carrega dados de uma aba específica"""
        try:
            range_name = f"{sheet_name}!{range_cells}"
            result = self.service.spreadsheets().values().get(
                spreadsheetId=settings.spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return pd.DataFrame()
            
            df = pd.DataFrame(values[1:], columns=values[0])
            return df.dropna(how='all')
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar dados da aba '{sheet_name}': {e}")
            st.error(f"Erro ao carregar dados: {e}")
            return pd.DataFrame()
    
    def get_all_sheets(self) -> List[str]:
        """Lista todas as abas da planilha"""
        try:
            metadata = self.service.spreadsheets().get(
                spreadsheetId=settings.spreadsheet_id
            ).execute()
            return [sheet['properties']['title'] for sheet in metadata.get('sheets', [])]
        except Exception as e:
            self.logger.error(f"Erro ao listar abas: {e}")
            return []

# Instância global
sheets_client = GoogleSheetsClient()