import sqlite3
import pandas as pd

conn = sqlite3.connect("retail_sales_analytics.db")

tables = ["customers", "orders", "products", "order_items", "payments"]

for table in tables:
    df = pd.read_sql_query(f"SELECT COUNT(*) AS count FROM {table}", conn)
    print(table, df["count"][0])

conn.close()
