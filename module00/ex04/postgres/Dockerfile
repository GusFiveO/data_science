FROM postgres:16

RUN apt update && apt install unzip

WORKDIR /docker-entrypoint-initdb.d

COPY --chown=postgres:postgres ./items_table.sql ./items_table.sql
ADD https://cdn.intra.42.fr/document/document/25745/subject.zip .

RUN unzip subject.zip 
