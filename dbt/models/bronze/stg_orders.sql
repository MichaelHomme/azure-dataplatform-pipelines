SELECT
    order_id,
    customer_id,
    CAST(order_date AS DATE) AS order_date,
    status,
    CAST(amount AS DECIMAL(10,2)) AS amount
FROM {{ ref('raw_orders') }}