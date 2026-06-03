SELECT
    o.order_id,
    o.customer_id,
    c.full_name,
    o.order_date,
    o.amount,
    o.status
FROM {{ ref('int_orders') }} o
INNER JOIN {{ ref('dim_customers') }} c
    ON o.customer_id = c.customer_id
WHERE o.status = 'completed'