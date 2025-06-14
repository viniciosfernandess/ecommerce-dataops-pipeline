# scripts/load.py

import os
import pandas as pd
from sqlalchemy import text
from db_connect import engine

def generate_metrics():
    """
    Lê a tabela staging.online_retail, calcula métricas por país e data,
    faz upsert em analytics.sales_summary e salva CSV em data/processed/.
    """
    # 1) Query para agregação na staging
    query = """
    SELECT
      Country AS country,
      DATE(InvoiceDate) AS invoice_date,
      SUM(Quantity) AS total_quantity,
      SUM(Quantity * UnitPrice) AS total_revenue
    FROM staging.online_retail
    GROUP BY Country, DATE(InvoiceDate)
    ORDER BY Country, DATE(InvoiceDate);
    """

    print("Lendo dados de staging para calcular métricas...")
    df = pd.read_sql(query, con=engine)

    # 2) Calcular ticket médio
    df["ticket_medio"] = df["total_revenue"] / df["total_quantity"]

    # 3) Upsert na tabela analytics.sales_summary
    print("Atualizando tabela analytics.sales_summary no banco...")
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(text("""
                INSERT INTO analytics.sales_summary
                    (country, invoice_date, total_quantity, total_revenue, ticket_medio)
                VALUES
                    (:country, :invoice_date, :total_quantity, :total_revenue, :ticket_medio)
                ON CONFLICT (country, invoice_date)
                DO UPDATE SET
                  total_quantity = EXCLUDED.total_quantity,
                  total_revenue  = EXCLUDED.total_revenue,
                  ticket_medio   = EXCLUDED.ticket_medio;
            """), {
                "country":        row["country"],
                "invoice_date":   row["invoice_date"],
                "total_quantity": int(row["total_quantity"]),
                "total_revenue":  float(row["total_revenue"]),
                "ticket_medio":   float(row["ticket_medio"])
            })
    print("Tabela analytics.sales_summary atualizada com sucesso.")

    # 4) Exportar CSV de métricas
    processed_dir = os.path.join(os.path.dirname(__file__), "../data/processed")
    os.makedirs(processed_dir, exist_ok=True)
    output_csv = os.path.join(processed_dir, "sales_summary.csv")
    df.to_csv(output_csv, index=False)
    print(f"CSV de métricas salvo em: {output_csv}")

if __name__ == "__main__":
    generate_metrics()
