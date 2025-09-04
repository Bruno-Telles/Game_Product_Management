# operational/utils/paths.py
import os
from pathlib import Path

# A partir deste arquivo, volta 3 níveis: operational/utils → operational → raiz
ROOT_DIR = Path(__file__).parent.parent.parent.resolve()

CONFIG_DIR = ROOT_DIR / "config"
DATA_DIR = ROOT_DIR / "data"
CREDENTIALS_PATH = CONFIG_DIR / "credentials.json"

def get_root():
    'Retorna a raiz do projeto.'
    return ROOT_DIR

def verify_project_structure():
    'Verifica se a estrutura de pastas está correta.'
    if not CREDENTIALS_PATH.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {CREDENTIALS_PATH}")
    return True