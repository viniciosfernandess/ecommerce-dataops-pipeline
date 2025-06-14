# scripts/test_db.py

from sqlalchemy import text
from db_connect import engine

# Executa uma query simples para testar a conexão
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1;"))
    print("Resultado da conexão:", result.scalar())