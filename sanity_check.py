import sqlite3

conn = sqlite3.connect("retail_sales_analytics.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM customers;")
count = cursor.fetchone()

print("Number of rows in customers table:", count[0])

cursor.execute("SELECT COUNT(*) FROM orders;")
count = cursor.fetchone()

print("Number of rows in orders table:", count[0])

cursor.execute("SELECT COUNT(*) FROM order_items;")
count = cursor.fetchone()

print("Number of rows in order_items table:", count[0])

cursor.execute("SELECT COUNT(*) FROM products;")
count = cursor.fetchone()

print("Number of rows in products table:", count[0])

cursor.execute("SELECT COUNT(*) FROM payments;")
count = cursor.fetchone()

print("Number of rows in payments table:", count[0])

conn.close()
