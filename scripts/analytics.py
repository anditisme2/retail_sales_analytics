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
    """,
    "orders_per_customer": """
        SELECT orders_count, COUNT(*) AS customers
        FROM ( SELECT c.customer_unique_id, COUNT(o.order_id) 
        AS orders_count
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_unique_id
        )
        GROUP BY orders_count
    ORDER BY orders_count;
    """,
    "repeat_behaviour": """
        WITH customer_orders AS (
        SELECT c.customer_unique_id, o.order_purchase_timestamp,
        ROW_NUMBER() OVER (
            PARTITION BY c.customer_unique_id
            ORDER BY o.order_purchase_timestamp
        ) AS order_rank
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        )
        SELECT ROUND(AVG(
        JULIANDAY(second.order_purchase_timestamp) -
        JULIANDAY(first.order_purchase_timestamp)
        ), 2) AS avg_days_between_orders
        FROM customer_orders first
        JOIN customer_orders second
        ON first.customer_unique_id = second.customer_unique_id
        WHERE first.order_rank = 1
        AND second.order_rank = 2;
    """,
    "monthly_order_volume": """
        SELECT STRFTIME('%Y-%m', order_purchase_timestamp) AS month,
        COUNT(order_id) AS total_orders
        FROM orders
        GROUP BY month
        ORDER BY month;
    """,
    "monthly_revenue_trend": """
        SELECT STRFTIME('%Y-%m', o.order_purchase_timestamp) AS month,
        ROUND(SUM(p.payment_value), 2) AS revenue
        FROM orders o
        JOIN payments p ON o.order_id = p.order_id
        GROUP BY month
        ORDER BY month;
    """,
    "one_time_vs_repeat_contri": """
        WITH customer_order_counts AS (
        SELECT c.customer_unique_id,
        COUNT(o.order_id) AS order_count
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_unique_id
        )
        SELECT CASE
        WHEN order_count = 1 THEN 'One-time'
        ELSE 'Repeat'
        END AS customer_type,
        ROUND(SUM(p.payment_value), 2) AS revenue
        FROM customer_order_counts coc
        JOIN customers c ON coc.customer_unique_id = c.customer_unique_id
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN payments p ON o.order_id = p.order_id
        GROUP BY customer_type;
    """
}
for name, q in queries.items():
    df = pd.read_sql_query(q, conn)
    print(f"\n{name.upper()}")
    print(df)

conn.close()