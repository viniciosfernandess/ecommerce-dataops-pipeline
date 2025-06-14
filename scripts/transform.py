# scripts/transform.py

import os
import pandas as pd
from sqlalchemy import text
from db_connect import engine


def transform_and_load():
    """
    Lê o CSV bruto, faz limpeza mínima de dados (nulos, tipos, datas),
    e carrega na tabela staging.online_retail.
    """
    # 1) Caminho do CSV bruto
    base_dir = os.path.dirname(__file__)
    raw_path = os.path.join(base_dir, "../data/raw/online_retail.csv")

    # 2) Leitura do CSV com pandas (forçando separador ';' e parser Python)
    print("Lendo CSV bruto em:", raw_path)
    df = pd.read_csv(
        raw_path,
        sep=';',                  # força ponto-e-vírgula
        encoding="ISO-8859-1",
        engine='python',          # parser mais tolerante
        dayfirst=True             # datas dia/mês/ano
    )

    # 3) Limpeza básica de nulos
    df = df.dropna(subset=["InvoiceNo", "StockCode", "InvoiceDate"])

    # 4) Conversões de tipo e ajuste decimal
    df["Quantity"] = df["Quantity"].astype(int)
    df["UnitPrice"] = (
        df["UnitPrice"]
          .astype(str)
          .str.replace(",", ".", regex=False)
          .astype(float)
    )

    # 5) Conversão e formatação de datas
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        dayfirst=True,
        errors="coerce"
    )
    df = df.dropna(subset=["InvoiceDate"])
    df["InvoiceDate"] = df["InvoiceDate"].dt.strftime("%Y-%m-%d %H:%M:%S")

    # 6) Selecionar colunas e converter nomes para lowercase (coincidir com tabelas no DB)
    df = df[[
        "InvoiceNo", "StockCode", "Description", "Quantity",
        "InvoiceDate", "UnitPrice", "CustomerID", "Country"
    ]]
    df.columns = df.columns.str.lower()

    # 7) Conectar ao banco e truncar/inserir
    print("Conectando ao banco e limpando staging.online_retail...")
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE staging.online_retail;"))
        print("Inserindo dados em staging.online_retail...")
        df.to_sql(
            name="online_retail",
            con=conn,
            schema="staging",
            if_exists="append",
            index=False
        )
    print("Transformação e carga na área de staging concluídas.")


if __name__ == "__main__":
    transform_and_load()
