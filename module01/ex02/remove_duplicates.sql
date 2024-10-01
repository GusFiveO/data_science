WITH ranked_customers AS (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY event_type, product_id, price, user_id, user_session 
                            ORDER BY event_time) AS rn
  FROM public.customers
)
DELETE FROM public.customers
WHERE (event_type, product_id, price, user_id, user_session, event_time) IN (
    SELECT event_type, product_id, price, user_id, user_session, event_time
    FROM ranked_customers
    WHERE rn > 1
);