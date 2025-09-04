#!/bin/bash
# scripts/deploy.sh

echo "🚀 Preparando deploy..."

# Testes
python -m pytest tests/ -v

# Linting
flake8 operational/ strategic/

# Deploy para Streamlit Cloud (se configurado)
git add .
git commit -m "Deploy: $(date)"
git push origin main

echo "✅ Deploy concluído!"