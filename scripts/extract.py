# scripts/extract.py

import os
import requests

def download_csv():
    """
    Baixa o arquivo CSV de vendas de e-commerce de uma URL pública
    e salva em data/raw/online_retail.csv.
    """
    # 1) URL pública do dataset
    RAW_URL = "https://raw.githubusercontent.com/erkansirin78/datasets/master/OnlineRetail.csv"
    
    # 2) Caminho local para salvar o arquivo
    base_dir = os.path.dirname(__file__)            # scripts/
    raw_dir  = os.path.join(base_dir, "../data/raw") 
    raw_path = os.path.join(raw_dir, "online_retail.csv")
    
    # 3) Garantir que a pasta data/raw exista
    os.makedirs(raw_dir, exist_ok=True)
    
    # 4) Fazer requisição HTTP GET
    print(f"Baixando dados de: {RAW_URL}")
    response = requests.get(RAW_URL)
    response.raise_for_status()  # interrompe em caso de erro HTTP
    
    # 5) Escrever conteúdo no arquivo local
    with open(raw_path, "wb") as f:
        f.write(response.content)
    print(f"Arquivo salvo em: {raw_path}")

if __name__ == "__main__":
    download_csv()
