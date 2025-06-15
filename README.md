# ecommerce-dataops-pipeline

**ETL DataOps Pipeline for E-Commerce Sales** automated via GitHub Actions.

[![ETL: Extract & Transform](https://github.com/viniciosfernandess/ecommerce-dataops-pipeline/actions/workflows/extract_transform.yml/badge.svg)](https://github.com/viniciosfernandess/ecommerce-dataops-pipeline/actions/workflows/extract_transform.yml)
[![ETL: Load & Report](https://github.com/viniciosfernandess/ecommerce-dataops-pipeline/actions/workflows/load_report.yml/badge.svg)](https://github.com/viniciosfernandess/ecommerce-dataops-pipeline/actions/workflows/load_report.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

---

## 🚀 Quick Start (Local Execution)

1. **Clone the repo**:
   ```bash
   git clone https://github.com/viniciosfernandess/ecommerce-dataops-pipeline.git
   cd ecommerce-dataops-pipeline
   ```
2. **Create Python virtual environment**:
   ```bash
   python -m venv .venv
   # Windows (Git Bash)
   source .venv/Scripts/activate
   # macOS/Linux
   # source .venv/bin/activate
   pip install --upgrade pip
   pip install pandas sqlalchemy psycopg2-binary matplotlib requests python-dotenv
   ```
3. **Configure database connection**:
   - Create a `.env` file in project root:
     ```dotenv
     DATABASE_URL=postgresql://postgres:<YOUR_PASSWORD>@localhost:5432/ecommerce_db
     ```
   - Ensure PostgreSQL is running and schemas/tables are created (see **Setup** instructions).
4. **Run full pipeline**:
   ```bash
   python scripts/extract.py
   python scripts/transform.py
   python scripts/aggregate.py    # optional if aggregated step is separate
   python scripts/load.py
   python scripts/report.py
   ```

---

## ⚙️ GitHub Actions Automation

Two scheduled workflows orchestrate the ETL and reporting process:

- **ETL: Extract & Transform**
  - **Schedule**: daily at 00:00 BRT
  - **Steps**: extract CSV → transform → load into `staging.online_retail`

- **ETL: Load & Report**
  - **Schedule**: daily at 02:00 BRT
  - **Steps**: read staging → compute metrics → load into `analytics.sales_summary` → export CSV → generate PNG reports → commit outputs back to repo

Workflows can also be manually triggered via **Actions** → select workflow → **Run workflow**.

---

## 📁 Project Structure

```text
.
├── .github/                # GitHub Actions workflows
│   └── workflows/
├── data/
│   ├── raw/               # Raw CSVs downloaded automatically
│   └── processed/         # Processed CSV metrics outputs
├── scripts/               # Python ETL and reporting scripts
│   └── logs/              # Optional execution logs
├── reports/               # Generated graph PNGs
├── README.md              # Project documentation (this file)
└── .gitignore             # Ignored files and folders
```

---

## 📌 About This Project

This pipeline demonstrates skills in:

- Building a robust **ETL** process with Python and SQL
- Implementing **DataOps** automation with **GitHub Actions**
- Managing relational databases (**PostgreSQL**)
- Generating automated **analytics** and **visualizations**

