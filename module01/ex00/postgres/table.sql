CREATE TABLE IF NOT EXISTS public.items (
	product_id integer NOT NULL,
	category_id	BIGINT,
	category_code character varying(255),
	brand character varying(255)
);


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

COPY public.items FROM '/docker-entrypoint-initdb.d/subject/item/item.csv' DELIMITER ',' CSV HEADER;

COPY public.data_2022_oct FROM '/docker-entrypoint-initdb.d/subject/customer/data_2022_oct.csv' DELIMITER ',' CSV HEADER;

COPY public.data_2022_nov FROM '/docker-entrypoint-initdb.d/subject/customer/data_2022_nov.csv' DELIMITER ',' CSV HEADER;

COPY public.data_2022_dec FROM '/docker-entrypoint-initdb.d/subject/customer/data_2022_dec.csv' DELIMITER ',' CSV HEADER;

COPY public.data_2023_jan FROM '/docker-entrypoint-initdb.d/subject/customer/data_2023_jan.csv' DELIMITER ',' CSV HEADER;