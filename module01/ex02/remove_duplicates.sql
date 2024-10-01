-- WITH ranked_customers AS (
--   SELECT *,
--          ROW_NUMBER() OVER (PARTITION BY event_type, product_id, price, user_id, user_session 
--                             ORDER BY event_time) AS rn
--   FROM public.customers
-- )
-- DELETE FROM public.customers
-- WHERE (event_type, product_id, price, user_id, user_session, event_time) IN (
--     SELECT event_type, product_id, price, user_id, user_session, event_time
--     FROM ranked_customers
--     WHERE rn > 1
-- );

DELETE FROM public.customers AS c1
WHERE EXISTS (
    SELECT 1
    FROM public.customers AS c2
    WHERE c1.event_type = c2.event_type
    AND c1.product_id = c2.product_id
    AND c1.price = c2.price
    AND c1.user_id = c2.user_id
    AND c1.user_session = c2.user_session
    AND (
        c1.event_time = c2.event_time
        OR c1.event_time = c2.event_time + interval '1 second'
    )
    -- AND c1.event_time > c2.event_time
);
