FROM postgres:16

# RUN apt update && apt install unzip

# ADD https://cdn.intra.42.fr/document/document/25745/subject.zip .

# RUN unzip subject.zip 

# ADD --chown=postgres:postgres https://cdn.intra.42.fr/document/document/17535/data_2023_feb.csv   /subject/customer/
COPY --chown=postgres:postgres ./initdb.sql /docker-entrypoint-initdb.d/initdb.sql
