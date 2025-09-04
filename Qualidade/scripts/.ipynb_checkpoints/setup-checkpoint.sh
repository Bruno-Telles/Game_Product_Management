#!/bin/bash
# scripts/setup.sh

echo "🚀 Configurando ambiente de desenvolvimento..."

# Cria ambiente virtual
python -m venv gpm_env
source gpm_env/bin/activate  # Linux/Mac
# gpm_env\Scripts\activate   # Windows

# Instala dependências
pip install -r requirements.txt

# Cria arquivos de configuração
cp config/credentials_example.json config/credentials.json
cp .env.example .env

echo "✅ Setup concluído! Configure suas credenciais em config/credentials.json"