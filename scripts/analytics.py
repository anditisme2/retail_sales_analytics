import sqlite3
import pandas as pd

conn = sqlite3.connect("../retail_sales_analytics.db")

queries = {
    "total_unique_customers": """
        SELECT COUNT(DISTINCT customer_unique_id) AS total_customers
        FROM customers;
    """,
    "repeat_customers": """
        SELECT COUNT(*) AS repeat_customers
        FROM (SELECT customer_unique_id
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY customer_unique_id
        HAVING COUNT(o.order_id) > 1
    );
    """,
    "percentage_of_repeat_customers": """
        SELECT ROUND(
        (COUNT(DISTINCT repeat.customer_unique_id) * 100.0) /
        COUNT(DISTINCT c.customer_unique_id), 2)
        AS repeat_customer_percentage
        FROM customers c
        LEFT JOIN (SELECT c.customer_unique_id
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_unique_id
        HAVING COUNT(o.order_id) > 1) 
        repeat ON c.customer_unique_id = repeat.customer_unique_id;
    """,
    "revenue_per_customer": """
        SELECT c.customer_unique_id,
        ROUND(SUM(p.payment_value), 2) AS total_spent
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN payments p ON o.order_id = p.order_id
        GROUP BY c.customer_unique_id
        ORDER BY total_spent DESC
        LIMIT 10;
    """,
    "average_per_customer": """
        SELECT ROUND(SUM(p.payment_value) / COUNT(DISTINCT c.customer_unique_id), 2)
        AS avg_revenue_per_customer
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN payments p ON o.order_id = p.order_id;
    """,
    "customer_distribution_by_state": """
        SELECT customer_state, COUNT(DISTINCT customer_unique_id) AS customers
        FROM customers
        GROUP BY customer_state
        ORDER BY customers DESC;
    """
}
for name, q in queries.items():
    df = pd.read_sql_query(q, conn)
    print(f"\n{name.upper()}")
    print(df)

conn.close()