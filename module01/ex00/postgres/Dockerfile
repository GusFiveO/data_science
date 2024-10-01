FROM postgres:16

RUN apt update && apt install unzip

COPY --chown=postgres:postgres ./items.sql /docker-entrypoint-initdb.d/items.sql
ADD https://cdn.intra.42.fr/document/document/25745/subject.zip .

RUN unzip subject.zip 

ADD --chown=postgres:postgres https://cdn.intra.42.fr/document/document/17535/data_2023_feb.csv /subject/customer/

COPY --chown=postgres:postgres ./automatic_table.sh .
RUN ./automatic_table.sh