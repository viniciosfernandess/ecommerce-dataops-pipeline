# scripts/db_connect.py

import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carrega variáveis de ambiente definidas no arquivo .env
load_dotenv()

# Lê a variável DATABASE_URL do ambiente
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("A variável DATABASE_URL não está definida no arquivo .env")

# DEBUG: mostra o valor lido de DATABASE_URL

# Cria o engine de conexão do SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)