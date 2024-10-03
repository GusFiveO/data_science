#!/bin/bash

csv_folder="/subject/customer"

db_name=$POSTGRES_DB
db_user=$POSTGRES_USER
db_password=$POSTGRES_PASSWORD

for csv_file in "$csv_folder"/*.csv; do
    echo "$csv_file"
    table_name=$(basename "$csv_file" .csv)

    echo "Creating table $table_name"

    sql="
    DROP TABLE IF EXISTS $table_name;
    CREATE TABLE $table_name (
    	event_time timestamp,
        event_type character varying(16) NOT NULL,
        product_id integer NOT NULL,
        price FLOAT NOT NULL,
        user_id BIGINT NOT NULL,
        user_session UUID
    );
    COPY $table_name FROM '$csv_file' DELIMITER ',' CSV HEADER;
    "

    echo $sql >> /docker-entrypoint-initdb.d/initdb.sql 
done
