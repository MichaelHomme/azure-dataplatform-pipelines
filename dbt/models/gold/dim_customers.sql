SELECT
    customer_id,
    first_name || ' ' || last_name AS full_name,
    email,
    signup_date
FROM {{ ref('int_customers') }}
WHERE customer_id IS NOT NULL