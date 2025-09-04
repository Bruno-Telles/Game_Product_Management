# operational/utils/sheets_client.py
import streamlit as st
import pandas as pd
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import Optional, List, Dict, Any
from datetime import datetime
import time

# Import das configurações
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.settings import settings

class GoogleSheetsClient:
    """Cliente profissional para Google Sheets com cache, retry e logging"""
    
    def __init__(self):
        self._service = None
        self.logger = logging.getLogger(__name__)
        self._last_request_time = 0
        self._min_request_interval = 0.1  # Rate limiting: 100ms entre requests
        
    @property
    def service(self):
        """Lazy loading do serviço Google Sheets com rate limiting"""
        if self._service is None:
            self._service = self._create_service()
        return self._service
    
    def _create_service(self):
        """Cria o serviço Google Sheets com tratamento de erro"""
        try:
            credentials_info = settings.get_google_credentials()
            creds = service_account.Credentials.from_service_account_info(
                credentials_info,
                scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
            )
            service = build('sheets', 'v4', credentials=creds)
            self.logger.info("✅ Serviço Google Sheets criado com sucesso")
            return service
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao criar serviço Google Sheets: {e}")
            raise ConnectionError(f"Falha na conexão com Google Sheets: {e}")
    
    def _rate_limit(self):
        """Implementa rate limiting simples"""
        current_time = time.time()
        time_since_last = current_time - self._last_request_time
        if time_since_last < self._min_request_interval:
            time.sleep(self._min_request_interval - time_since_last)
        self._last_request_time = time.time()
    
    @st.cache_data(ttl=settings.cache_ttl, show_spinner="Carregando dados...")
    def get_sheet_data(_self, sheet_name: str, range_cells: Optional[str] = None) -> pd.DataFrame:
        """
        Carrega dados de uma aba específica com cache e validação
        
        Args:
            sheet_name: Nome da aba
            range_cells: Range específico (ex: A1:E100)
            
        Returns:
            DataFrame com os dados
        """
        try:
            # Rate limiting
            _self._rate_limit()
            
            # Usa range da configuração se não especificado
            if range_cells is None:
                sheet_config = settings.get_sheet_config(sheet_name)
                range_cells = sheet_config['range'] if sheet_config else 'A1:Z1000'
            
            range_name = f"{sheet_name}!{range_cells}"
            
            _self.logger.info(f"📊 Carregando dados: {range_name}")
            
            result = _self.service.spreadsheets().values().get(
                spreadsheetId=settings.spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                _self.logger.warning(f"⚠️ Nenhum dado encontrado em {sheet_name}")
                return pd.DataFrame()
            
            if len(values) == 1:
                _self.logger.warning(f"⚠️ Apenas cabeçalho encontrado em {sheet_name}")
                return pd.DataFrame(columns=values[0])
            
            # Cria DataFrame
            df = pd.DataFrame(values[1:], columns=values[0])
            
            # Limpeza básica
            df = df.dropna(how='all')  # Remove linhas completamente vazias
            df.columns = df.columns.str.strip()  # Remove espaços dos nomes das colunas
            
            # Validação das colunas obrigatórias
            sheet_config = settings.get_sheet_config(sheet_name)
            if sheet_config and sheet_config['required_columns']:
                missing_cols = set(sheet_config['required_columns']) - set(df.columns)
                if missing_cols:
                    _self.logger.warning(f"⚠️ Colunas faltando em {sheet_name}: {missing_cols}")
            
            _self.logger.info(f"✅ Dados carregados: {len(df)} linhas, {len(df.columns)} colunas")
            return df
            
        except HttpError as e:
            error_msg = f"Erro HTTP ao acessar {sheet_name}: {e}"
            _self.logger.error(error_msg)
            st.error(f"❌ {error_msg}")
            return pd.DataFrame()
            
        except Exception as e:
            error_msg = f"Erro inesperado ao carregar {sheet_name}: {e}"
            _self.logger.error(error_msg)
            st.error(f"❌ {error_msg}")
            return pd.DataFrame()
    
    @st.cache_data(ttl=600)  # Cache por 10 minutos
    def get_all_sheets(_self) -> List[Dict[str, Any]]:
        """
        Lista todas as abas da planilha com metadados
        
        Returns:
            Lista com informações das abas
        """
        try:
            _self._rate_limit()
            
            metadata = _self.service.spreadsheets().get(
                spreadsheetId=settings.spreadsheet_id
            ).execute()
            
            sheets_info = []
            for sheet in metadata.get('sheets', []):
                props = sheet['properties']
                sheet_name = props['title']
                sheet_config = settings.get_sheet_config(sheet_name)
                
                sheets_info.append({
                    'name': sheet_name,
                    'display_name': sheet_config['display_name'] if sheet_config else sheet_name,
                    'icon': sheet_config['icon'] if sheet_config else '📊',
                    'rows': props.get('gridProperties', {}).get('rowCount', 0),
                    'columns': props.get('gridProperties', {}).get('columnCount', 0)
                })
            
            return sheets_info
            
        except Exception as e:
            error_msg = f"Erro ao listar abas: {e}"
            _self.logger.error(error_msg)
            st.error(f"❌ {error_msg}")
            return []
    
    def health_check(self) -> Dict[str, Any]:
        """
        Verifica a saúde da conexão com Google Sheets
        
        Returns:
            Dicionário com status da conexão
        """
        health_status = {
            'timestamp': datetime.now(),
            'service_available': False,
            'sheets_accessible': False,
            'sheets_count': 0,
            'error_message': None
        }
        
        try:
            # Testa criação do serviço
            _ = self.service
            health_status['service_available'] = True
            
            # Testa acesso às planilhas
            sheets = self.get_all_sheets()
            if sheets:
                health_status['sheets_accessible'] = True
                health_status['sheets_count'] = len(sheets)
            
            self.logger.info("✅ Health check passou")
            
        except Exception as e:
            health_status['error_message'] = str(e)
            self.logger.error(f"❌ Health check falhou: {e}")
        
        return health_status
    
    def clear_cache(self):
        """Limpa todo o cache do cliente"""
        st.cache_data.clear()
        self.logger.info("🧹 Cache limpo")

# Instância global do cliente
sheets_client = GoogleSheetsClient()

# Função de conveniência para compatibilidade com código existente
def get_sheet_data(spreadsheet_id: str, sheet_name: str, range_cells: str = "A1:Z1000") -> pd.DataFrame:
    """Função de compatibilidade - use sheets_client.get_sheet_data() diretamente"""
    return sheets_client.get_sheet_data(sheet_name, range_cells)

if __name__ == "__main__":
    # Teste do cliente
    print("🧪 Testando GoogleSheetsClient...")
    
    # Health check
    health = sheets_client.health_check()
    print(f"Status: {health}")
    
    # Lista abas
    sheets = sheets_client.get_all_sheets()
    for sheet in sheets:
        print(f"  {sheet['icon']} {sheet['display_name']}: {sheet['rows']}x{sheet['columns']}")
    
    # Testa carregamento de dados
    if sheets:
        df = sheets_client.get_sheet_data('Cohort')
        print(f"\nDados de Cohort: {len(df)} linhas")
        if not df.empty:
            print(f"Colunas: {list(df.columns)}")