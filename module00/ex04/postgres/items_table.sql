CREATE TABLE IF NOT EXISTS public.items (
	product_id integer NOT NULL,
	category_id	BIGINT,
	category_code character varying(255),
	brand character varying(255)
);

COPY public.items FROM '/docker-entrypoint-initdb.d/subject/item/item.csv' DELIMITER ',' CSV HEADER;