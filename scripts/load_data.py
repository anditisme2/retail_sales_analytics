import sqlite3
import pandas as pd

DB_PATH = "../retail_sales_analytics.db"

FILES = {
    "customers": "../data/raw/customers.csv",
    "orders": "../data/raw/orders.csv",
    "products": "../data/raw/products.csv",
    "order_items": "../data/raw/order_items.csv",
    "payments": "../data/raw/payments.csv"
}

conn = sqlite3.connect(DB_PATH)

for table, path in FILES.items():
    print(f"Loading {table}...")
    df = pd.read_csv(path)
    df.to_sql(table, conn, if_exists="append", index=False)

conn.close()
print("All data loaded successfully.")
