# test_credentials.py - Execute este arquivo para testar suas credenciais
import json
import os
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Caminho para o credentials.json
config_path = Path("config/credentials.json")

def test_credentials():
    print("🔍 Testando credenciais do Google Sheets...")
    print(f"📁 Procurando arquivo em: {config_path.absolute()}")
    
    # Verifica se o arquivo existe
    if not config_path.exists():
        print("❌ Arquivo credentials.json não encontrado!")
        print(f"   Caminho esperado: {config_path.absolute()}")
        return False
    
    print("✅ Arquivo credentials.json encontrado!")
    
    try:
        # Carrega o JSON
        with open(config_path, 'r', encoding='utf-8') as f:
            credentials_json = json.load(f)
        
        print("✅ Arquivo JSON válido!")
        
        # Verifica campos obrigatórios
        required_fields = ['type', 'client_email', 'private_key', 'project_id']
        for field in required_fields:
            if field not in credentials_json:
                print(f"❌ Campo obrigatório '{field}' não encontrado no JSON!")
                return False
        
        print("✅ Todos os campos obrigatórios presentes!")
        
        # Tenta criar as credenciais
        creds = service_account.Credentials.from_service_account_info(
            credentials_json,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        
        print("✅ Credenciais criadas com sucesso!")
        
        # Tenta conectar ao Google Sheets API
        service = build('sheets', 'v4', credentials=creds)
        print("✅ Conexão com Google Sheets API estabelecida!")
        
        # Testa acesso à planilha específica
        spreadsheet_id = "15k4L7Sib0ZRTWfeo_wgR5F4YLGQkGEiPZPSPFjwZHHw"
        
        try:
            # Tenta ler metadados da planilha
            sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            print("✅ Acesso à planilha confirmado!")
            
            sheets = sheet_metadata.get('sheets', [])
            print(f"📊 Abas encontradas: {[sheet['properties']['title'] for sheet in sheets]}")
            
            # Testa leitura de dados da aba Cohort
            try:
                result = service.spreadsheets().values().get(
                    spreadsheetId=spreadsheet_id,
                    range="Cohort!A1:Z10"
                ).execute()
                
                values = result.get('values', [])
                if values:
                    print(f"✅ Dados da aba 'Cohort': {len(values)} linhas encontradas")
                    print(f"   Cabeçalho: {values[0] if values else 'Vazio'}")
                else:
                    print("⚠️  Aba 'Cohort' está vazia")
                    
            except Exception as e:
                print(f"❌ Erro ao ler aba 'Cohort': {e}")
            
            # Testa leitura de dados da aba Monetization
            try:
                result = service.spreadsheets().values().get(
                    spreadsheetId=spreadsheet_id,
                    range="Monetization!A1:Z10"
                ).execute()
                
                values = result.get('values', [])
                if values:
                    print(f"✅ Dados da aba 'Monetization': {len(values)} linhas encontradas")
                    print(f"   Cabeçalho: {values[0] if values else 'Vazio'}")
                else:
                    print("⚠️  Aba 'Monetization' está vazia")
                    
            except Exception as e:
                print(f"❌ Erro ao ler aba 'Monetization': {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao acessar planilha: {e}")
            print("   Verifique se:")
            print("   - A planilha existe e está acessível")
            print("   - A planilha foi compartilhada com o email de serviço")
            return False
        
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao decodificar JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    success = test_credentials()
    if success:
        print("\n🎉 Teste concluído com sucesso! O Streamlit deve funcionar agora.")
    else:
        print("\n💡 Corrija os erros acima antes de executar o Streamlit.")