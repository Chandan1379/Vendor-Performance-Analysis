# Vendor Performance Analysis

## 📌 Project Overview
This project focuses on analyzing vendor performance by consolidating data from multiple sources, including purchases, sales, and freight costs. The goal is to evaluate vendors based on profitability, efficiency, and sales contribution using both Python and Power BI.

## 🧰 Tools & Technologies
- **Python**: Data processing and cleaning (pandas, sqlite3)
- **SQL (SQLite)**: Data querying and summarization
- **Power BI**: Data visualization and dashboard creation
- **Jupyter Notebook**: Exploratory data analysis and prototyping
- **Logging**: Execution traceability for debugging

## 📁 Project Structure
```
├── data/                       # Input CSV/Excel files (not included in repo)
├── logs/                       # Execution logs
├── ingestion_db.py             # Script to ingest data into SQLite DB
├── get_vendor_summary.py       # SQL logic + data cleaning + metrics calculation
├── Vendor Performance Analysis.ipynb  # EDA and visual exploration
├── dashboard.pbix              # Power BI dashboard (optional if large)
└── README.md                   # Project documentation
```

## 🔄 Workflow Summary
1. **Data Ingestion**: CSV files ingested into SQLite using `ingestion_db.py`.
2. **SQL Querying**: Custom CTEs used to calculate purchase summaries, sales data, and freight costs.
3. **Data Cleaning**: Handling missing values, data types, and formatting.
4. **Feature Engineering**: Computed KPIs like profit margin, stock turnover, and sales-to-purchase ratio.
5. **Dashboarding**: Final metrics visualized in Power BI.

## 📊 Key Metrics
- **Gross Profit** = Sales Revenue − Purchase Cost
- **Profit Margin (%)** = Gross Profit ÷ Sales Revenue
- **Stock Turnover** = Sales Quantity ÷ Purchase Quantity
- **Sales-to-Purchase Ratio** = Sales Dollars ÷ Purchase Dollars

## ✅ Insights
- Identified top and low-performing vendors based on KPIs
- Visualized vendor-level performance with brand segmentation
- Highlighted vendors with high freight costs affecting margins

## ⚙️ How to Run
1. Place raw `.csv` data files in a `data/` directory.
2. Run `ingestion_db.py` to ingest data into SQLite.
3. Execute `get_vendor_summary.py` to generate the summary table and KPIs.
4. Open `Vendor Performance Analysis.ipynb` for interactive exploration.
5. Open `dashboard.pbix` in Power BI to view visualizations.

## 🧹 Data Handling
- Missing values filled with zeros where applicable.
- Removed trailing/leading spaces from text fields.
- Logging enabled for transparency in each step.

## 📌 Note
Data files are excluded for privacy. You may add sample data if needed for reproducibility.

---
