import sqlite3
import pandas as pd

conn = sqlite3.connect("../retail_sales_analytics.db")

queries = {
    "total_revenue": """
        SELECT ROUND(SUM(payment_value), 2) AS total_revenue
        FROM payments;
    """,
    "revenue_by_payment": """
        SELECT payment_type, ROUND(SUM(payment_value), 2) AS revenue
        FROM payments
        GROUP BY payment_type
        ORDER BY revenue DESC;
    """,
    "total_orders":"""
        SELECT COUNT(DISTINCT order_id) AS total_orders 
        FROM orders;
    """,
    "orders_over_time":"""
       SELECT DATE(order_purchase_timestamp) AS order_date, COUNT(order_id) AS orders 
       FROM orders 
       GROUP BY order_date 
       ORDER BY order_date; 
    """,
    "revenue_by_product":"""
        SELECT p.product_category_name, ROUND(SUM(oi.price), 2) AS revenue 
        FROM order_items oi 
        JOIN products p 
        ON oi.product_id = p.product_id 
        GROUP BY p.product_category_name 
        ORDER BY revenue DESC 
        LIMIT 10;
    """
}

for name, q in queries.items():
    df = pd.read_sql_query(q, conn)
    print(f"\n{name.upper()}")
    print(df)

conn.close()
