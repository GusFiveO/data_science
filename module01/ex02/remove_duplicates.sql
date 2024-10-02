CREATE TEMP TABLE temp_customers_to_keep (LIKE customers);
INSERT INTO temp_customers_to_keep SELECT DISTINCT ON (event_type, product_id, price, user_id, user_session, DATE_TRUNC('minute', event_time))
	event_time, event_type, product_id, price, user_id, user_session
FROM customers;

TRUNCATE customers;

INSERT INTO customers
SELECT * FROM temp_customers_to_keep;