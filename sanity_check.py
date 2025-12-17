import sqlite3

conn = sqlite3.connect("retail_sales_analytics.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM customers;")
count = cursor.fetchone()

print("Number of rows in customers table:", count[0])

conn.close()
