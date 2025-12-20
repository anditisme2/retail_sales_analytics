SELECT MAX(order_purchase_timestamp) FROM orders;
WITH customer_orders AS (
    SELECT
        c.customer_unique_id,
        o.order_id,
        o.order_purchase_timestamp,
        p.payment_value
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN payments p ON o.order_id = p.order_id
),

rfm_base AS (
    SELECT
        customer_unique_id,
        MAX(order_purchase_timestamp) AS last_purchase_date,
        COUNT(DISTINCT order_id) AS frequency,
        SUM(payment_value) AS monetary
    FROM customer_orders
    GROUP BY customer_unique_id
)

SELECT
    customer_unique_id,

    -- Recency (days since last purchase)
    JULIANDAY((SELECT MAX(order_purchase_timestamp) FROM orders))
    - JULIANDAY(last_purchase_date) AS recency,

    frequency,
    monetary
FROM rfm_base;
