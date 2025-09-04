# GAME PRODUCT MANAGEMENT
Dashboard para análise de jogos diretamente do Google Sheets e/ou Faker.

## Como usar

    1. Crie um arquivo 'credentials.json' (veja instruções abaixo)
    2. Coloque no 'config/'
    3. Altere o 'sheet_id' no 'streamlit_app.py'
    4. Rode: 'streamlit run streamlit_app.py'

## Como gerar credentials.json

    1. Acesse: https://console.cloud.google.com/
    2. Crie um projeto
    3. Ative a API do Google Sheets
    4. Crie uma conta de serviço
    5. Baixe o JSON e renomeie para 'credentials.json'

    Mais detalhes: https://gspread.readthedocs.io/en/latest/


# 🏗️ Estrutura Profissional para Game Product Management Dashboard

## 📁 Estrutura de Arquivos Recomendada

```
Game_Product_Management/
├── 📋 Configuração
│   ├── .env                          # Variáveis de ambiente (LOCAL)
│   ├── .env.example                  # Exemplo das variáveis
│   ├── config/
│   │   ├── settings.py               # Configurações centralizadas
│   │   ├── credentials.json          # Credenciais Google (LOCAL)
│   │   └── credentials_example.json  # Exemplo das credenciais
│   └── .streamlit/
│       └── secrets.toml              # Secrets do Streamlit (PRODUÇÃO)
├── 🚀 Aplicação
│   ├── main.py                       # Ponto de entrada principal
│   ├── operational/
│   │   ├── streamlit_app.py          # App Streamlit
│   │   ├── dashboards/               # Dashboards modulares
│   │   ├── components/               # Componentes reutilizáveis
│   │   └── utils/                    # Utilitários
│   └── strategic/                    # Análises estratégicas
├── 📊 Dados
│   ├── data/
│   │   ├── raw/                      # Dados brutos
│   │   ├── processed/                # Dados processados
│   │   └── exports/                  # Exportações
│   └── notebooks/                    # Jupyter notebooks para análise
├── 🧪 Qualidade
│   ├── tests/                        # Testes automatizados
│   ├── docs/                         # Documentação
│   └── scripts/                      # Scripts de automação
└── 🔧 DevOps
    ├── docker/                       # Containerização
    ├── .github/workflows/            # CI/CD
    └── deployment/                   # Scripts de deploy
```
