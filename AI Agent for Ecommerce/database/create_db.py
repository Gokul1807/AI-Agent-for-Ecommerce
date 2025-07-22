import pandas as pd
import sqlite3

# File paths
excel_files = {
    "ad_sales_metrics": r"D:\Fifth Year (2025-26)\Project for Anarx\AI Agent for Ecommerce\data\Product-Level Ad Sales and Metrics (mapped).xlsx",
    "total_sales_metrics": r"D:\Fifth Year (2025-26)\Project for Anarx\AI Agent for Ecommerce\data\Product-Level Total Sales and Metrics (mapped).xlsx",
    "eligibility_table": r"D:\Fifth Year (2025-26)\Project for Anarx\AI Agent for Ecommerce\data\Product-Level Eligibility Table (mapped).xlsx"
}

# SQLite database file
sqlite_db = "ecommerce.db"

# Connect to SQLite
conn = sqlite3.connect(sqlite_db)

# Load and insert each Excel file
for table_name, file_path in excel_files.items():
    print(f"Loading {table_name} from {file_path}")
    
    df = pd.read_excel(file_path)

    # Normalize column names to avoid issues
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Insert into SQLite table (replace if exists)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Inserted {len(df)} rows into table '{table_name}'")

conn.close()
print(" All data loaded into SQLite successfully!")
