import sqlite3
import pandas as pd

conn=sqlite3.connect("../retail_sales_analytics.db")

df=pd.read_csv("../data/raw/customers.csv")
df.to_sql("customers", conn, if_exists="append", index=False)
print(df.columns.tolist())

conn.close()

print("Customers loaded successfully.")