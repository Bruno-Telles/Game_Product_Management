# config/settings.py
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

class Settings:
    """Configurações centralizadas do projeto"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.environment = os.getenv('ENVIRONMENT', 'development')
        self._setup_logging()
        
    def _setup_logging(self):
        """Configura logging do projeto"""
        logging.basicConfig(
            level=logging.INFO if self.environment == 'production' else logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def get_google_credentials(self) -> Dict[str, Any]:
        """Carrega credenciais do Google Sheets baseado no ambiente"""
        try:
            if self.environment == 'production':
                # Streamlit Cloud - usa st.secrets
                import streamlit as st
                credentials_str = st.secrets["google_sheets"]["credentials_json"]
                return json.loads(credentials_str) if isinstance(credentials_str, str) else credentials_str
            else:
                # Desenvolvimento local - usa arquivo JSON
                creds_path = self.project_root / "config" / "credentials.json"
                if not creds_path.exists():
                    raise FileNotFoundError(f"Credenciais não encontradas: {creds_path}")
                    
                with open(creds_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
                    
        except Exception as e:
            self.logger.error(f"Erro ao carregar credenciais: {e}")
            raise
    
    @property
    def spreadsheet_id(self) -> str:
        """ID da planilha principal"""
        return os.getenv('GOOGLE_SPREADSHEET_ID', 
                        '15k4L7Sib0ZRTWfeo_wgR5F4YLGQkGEiPZPSPFjwZHHw')
    
    @property
    def cache_ttl(self) -> int:
        """Tempo de cache em segundos"""
        return int(os.getenv('CACHE_TTL', '300'))  # 5 minutos default
    
    @property
    def debug_mode(self) -> bool:
        """Modo debug ativo"""
        return os.getenv('DEBUG', 'False').lower() == 'true'
    
    @property
    def available_sheets(self) -> list:
        """Lista de abas disponíveis na planilha"""
        return ['Cohort', 'Monetization', 'Convertion']
    
    def get_sheet_config(self, sheet_name: str) -> Optional[Dict[str, Any]]:
        """Configurações específicas por aba"""
        configs = {
            'Cohort': {
                'range': 'A1:E100',
                'required_columns': ['COHORT', 'USERS', 'RETENTION_D1', 'RETENTION_D7', 'RETENTION_D30'],
                'display_name': 'Análise de Coorte',
                'icon': '📈'
            },
            'Monetization': {
                'range': 'A1:E100', 
                'required_columns': ['INSTALL_DATE', 'REVENUE', 'DAU', 'ARPU', 'CONVERTION'],
                'display_name': 'Monetização',
                'icon': '💰'
            },
            'Convertion': {
                'range': 'A1:Z100',
                'required_columns': [],
                'display_name': 'Conversão',
                'icon': '🎯'
            }
        }
        return configs.get(sheet_name)

# Instância global das configurações
settings = Settings()

# Validação na importação
if __name__ == "__main__":
    print(f"🔧 Configurações carregadas:")
    print(f"   Ambiente: {settings.environment}")
    print(f"   Debug: {settings.debug_mode}")
    print(f"   Cache TTL: {settings.cache_ttl}s")
    print(f"   Planilha ID: {settings.spreadsheet_id}")
    print(f"   Abas disponíveis: {settings.available_sheets}")
    
    try:
        creds = settings.get_google_credentials()
        print(f"   ✅ Credenciais: {creds.get('client_email', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Erro nas credenciais: {e}")