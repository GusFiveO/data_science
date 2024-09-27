CREATE TABLE IF NOT EXISTS public.data_2022_oct (
	event_time timestamp,
	event_type character varying(16) NOT NULL,
	product_id integer NOT NULL,
	price FLOAT NOT NULL,
	user_id BIGINT NOT NULL,
	user_session UUID
);

COPY public.data_2022_oct FROM '/docker-entrypoint-initdb.d/subject/customer/data_2022_oct.csv' DELIMITER ',' CSV HEADER;