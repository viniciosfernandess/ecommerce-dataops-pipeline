# scripts/report.py

import os
import pandas as pd
import matplotlib.pyplot as plt
from db_connect import engine

def generate_report():
    """
    Lê a tabela analytics.sales_summary, plota a série temporal
    de receita global diária e salva o PNG em ../reports/.
    """
    # 1) Carregar métricas consolidadas
    query = """
    SELECT
      invoice_date,
      SUM(total_revenue) AS revenue_global
    FROM analytics.sales_summary
    GROUP BY invoice_date
    ORDER BY invoice_date;
    """
    print("Carregando métricas para relatório...")
    df = pd.read_sql(query, con=engine)
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])

    # 2) Plotar
    plt.figure(figsize=(10, 6))
    plt.plot(df["invoice_date"], df["revenue_global"], marker="o")
    plt.title("Receita Global Diária - E-commerce")
    plt.xlabel("Data")
    plt.ylabel("Receita (monetária)")
    plt.grid(True)

    # 3) Salvar PNG
    reports_dir = os.path.join(os.path.dirname(__file__), "../reports")
    os.makedirs(reports_dir, exist_ok=True)
    output_path = os.path.join(reports_dir, "revenue_timeseries.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Gráfico salvo em: {output_path}")

if __name__ == "__main__":
    generate_report()
