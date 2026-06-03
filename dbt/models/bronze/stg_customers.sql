-- Simple 1:1 read from the raw seed, casting types if necessary
SELECT
    customer_id,
    first_name,
    last_name,
    email,
    CAST(signup_date AS DATE) AS signup_date
FROM {{ ref('raw_customers') }}