CREATE TABLE IF NOT EXISTS public.items (
	product_id integer NOT NULL,
	category_id	BIGINT,
	category_code character varying(255),
	brand character varying(255)
);


COPY public.items FROM '/subject/item/item.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE IF NOT EXISTS public.data_2022_oct (
	event_time timestamp,
	event_type character varying(16) NOT NULL,
	product_id integer NOT NULL,
	price FLOAT NOT NULL,
	user_id BIGINT NOT NULL,
	user_session UUID
);
CREATE TABLE IF NOT EXISTS public.data_2022_nov (
	event_time timestamp,
	event_type character varying(16) NOT NULL,
	product_id integer NOT NULL,
	price FLOAT NOT NULL,
	user_id BIGINT NOT NULL,
	user_session UUID
);
CREATE TABLE IF NOT EXISTS public.data_2022_dec (
	event_time timestamp,
	event_type character varying(16) NOT NULL,
	product_id integer NOT NULL,
	price FLOAT NOT NULL,
	user_id BIGINT NOT NULL,
	user_session UUID
);
CREATE TABLE IF NOT EXISTS public.data_2023_jan (
	event_time timestamp,
	event_type character varying(16) NOT NULL,
	product_id integer NOT NULL,
	price FLOAT NOT NULL,
	user_id BIGINT NOT NULL,
	user_session UUID
);
CREATE TABLE IF NOT EXISTS public.data_2023_feb (
	event_time timestamp,
	event_type character varying(16) NOT NULL,
	product_id integer NOT NULL,
	price FLOAT NOT NULL,
	user_id BIGINT NOT NULL,
	user_session UUID
);
COPY public.data_2022_oct FROM '/subject/customer/data_2022_oct.csv' DELIMITER ',' CSV HEADER;
COPY public.data_2022_nov FROM '/subject/customer/data_2022_nov.csv' DELIMITER ',' CSV HEADER;
COPY public.data_2022_dec FROM '/subject/customer/data_2022_dec.csv' DELIMITER ',' CSV HEADER;
COPY public.data_2023_jan FROM '/subject/customer/data_2023_jan.csv' DELIMITER ',' CSV HEADER;
COPY public.data_2023_feb FROM '/subject/customer/data_2023_feb.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE customers as
        SELECT * FROM data_2022_oct
        UNION ALL
        SELECT * FROM data_2022_nov
        UNION ALL
        SELECT * FROM data_2022_dec
        UNION ALL
        SELECT * FROM data_2023_jan
        UNION ALL
        SELECT * FROM data_2023_feb;


CREATE TEMP TABLE temp_customers_to_keep (LIKE customers);
INSERT INTO temp_customers_to_keep SELECT DISTINCT ON (event_type, product_id, price, user_id, user_session, DATE_TRUNC('minute', event_time))
        event_time, event_type, product_id, price, user_id, user_session
FROM customers;

TRUNCATE customers;

INSERT INTO customers
SELECT * FROM temp_customers_to_keep;

ALTER TABLE public.customers
ADD COLUMN category_ids BIGINT[],
ADD COLUMN category_codes character varying(255)[],
ADD COLUMN brands character varying(255)[];


WITH non_null_items AS (
    SELECT 
        product_id,
        ARRAY_AGG(DISTINCT category_id) FILTER (WHERE category_id IS NOT NULL) AS category_ids,
        ARRAY_AGG(DISTINCT category_code) FILTER (WHERE category_code IS NOT NULL) AS category_codes,
        ARRAY_AGG(DISTINCT brand) FILTER (WHERE brand IS NOT NULL) AS brands
    FROM public.items
    GROUP BY product_id
)

UPDATE public.customers AS customers
SET
    category_ids = non_null_items.category_ids,
    category_codes = non_null_items.category_codes,
    brands = non_null_items.brands
FROM non_null_items
WHERE customers.product_id = non_null_items.product_id;
