import sqlite3

conn = sqlite3.connect("retail_sales_analytics.db")

with open("sql/schema.sql", "r") as f:
    schema = f.read()

conn.executescript(schema)
conn.close()

print("Database and tables created successfully.")
