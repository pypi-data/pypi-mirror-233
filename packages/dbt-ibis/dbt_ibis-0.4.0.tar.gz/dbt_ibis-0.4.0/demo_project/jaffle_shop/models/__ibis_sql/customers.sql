WITH t1 AS (
  SELECT
    t6.customer_id AS customer_id,
    MIN(t6.order_date) AS first_order,
    MAX(t6.order_date) AS most_recent_order,
    COUNT(*) AS number_of_orders
  FROM {{ ref('stg_orders') }} AS t6
  GROUP BY
    1
), t3 AS (
  SELECT
    t6.customer_id AS customer_id,
    t6.first_name AS first_name,
    t6.last_name AS last_name,
    t1.customer_id AS customer_id_right,
    t1.first_order AS first_order,
    t1.most_recent_order AS most_recent_order,
    t1.number_of_orders AS number_of_orders
  FROM {{ ref('stg_customers') }} AS t6
  LEFT OUTER JOIN t1
    ON t6.customer_id = t1.customer_id
), t0 AS (
  SELECT
    t6.payment_id AS payment_id,
    t6.order_id AS order_id,
    t6.payment_method AS payment_method,
    t6.amount AS amount,
    t7.order_id AS order_id_right,
    t7.customer_id AS customer_id,
    t7.order_date AS order_date,
    t7.status AS status
  FROM {{ ref('stg_payments') }} AS t6
  LEFT OUTER JOIN {{ ref('stg_orders') }} AS t7
    ON t6.order_id = t7.order_id
), t2 AS (
  SELECT
    t0.customer_id AS customer_id,
    SUM(t0.amount) AS total_amount
  FROM t0
  GROUP BY
    1
), t4 AS (
  SELECT
    t3.customer_id AS customer_id,
    t3.first_name AS first_name,
    t3.last_name AS last_name,
    t3.customer_id_right AS customer_id_right,
    t3.first_order AS first_order,
    t3.most_recent_order AS most_recent_order,
    t3.number_of_orders AS number_of_orders,
    t2.customer_id AS customer_id_right2,
    t2.total_amount AS total_amount
  FROM t3
  LEFT OUTER JOIN t2
    ON t3.customer_id = t2.customer_id
)
SELECT
  t5.customer_id,
  t5.first_name,
  t5.last_name,
  t5.first_order,
  t5.most_recent_order,
  t5.number_of_orders,
  t5.customer_lifetime_value
FROM (
  SELECT
    t4.customer_id AS customer_id,
    t4.first_name AS first_name,
    t4.last_name AS last_name,
    t4.customer_id_right AS customer_id_right,
    t4.first_order AS first_order,
    t4.most_recent_order AS most_recent_order,
    t4.number_of_orders AS number_of_orders,
    t4.customer_id_right2 AS customer_id_right2,
    t4.total_amount AS customer_lifetime_value
  FROM t4
) AS t5