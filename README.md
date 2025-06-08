# ecommerce-dataops-pipeline
Pipeline ETL de vendas de e-commerce com DataOps, agendado via GitHub Actions.

## Funcionalidades

- Coleta diária de dados públicos de e-commerce (CSV)
- Limpeza e carga em tabela staging (PostgreSQL)
- Cálculo de métricas (vendas, ticket médio, top produtos)
- Geração de relatórios gráficos (PNG)
- Automação através de GitHub Actions (jobs às 00:00 e 02:00 BRT)

## Estrutura de Pastas
├── .github/
│ └── workflows/ # arquivos de workflow do GitHub Actions
├── data/
│ ├── raw/ # CSVs brutos baixados automaticamente
│ └── processed/ # CSVs de métricas gerados
├── scripts/ # scripts Python de ETL e report
├── reports/ # gráficos gerados em PNG
├── README.md # documentação do projeto
└── .gitignore # arquivos ignorados pelo Git