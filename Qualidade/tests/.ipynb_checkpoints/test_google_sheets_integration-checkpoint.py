# tests/test_google_sheets_integration.py
import pytest
from operational.utils.google_sheets_client import sheets_client

class TestGoogleSheetsIntegration:
    def test_connection(self):
        """Testa conexão com Google Sheets"""
        sheets = sheets_client.get_all_sheets()
        assert len(sheets) > 0
        assert 'Cohort' in sheets
        assert 'Monetization' in sheets
    
    def test_cohort_data_loading(self):
        """Testa carregamento de dados de coorte"""
        df = sheets_client.get_sheet_data('Cohort')
        assert not df.empty
        assert 'COHORT' in df.columns
    
    def test_monetization_data_loading(self):
        """Testa carregamento de dados de monetização"""
        df = sheets_client.get_sheet_data('Monetization')
        assert not df.empty
        assert 'REVENUE' in df.columns