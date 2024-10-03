FROM postgres:16

# RUN apt update && apt install unzip
# RUN apt update && apt install python3 python3-psycopg2-binary -y && apt install python3-pip -y
# RUN pip3 install psycopg2-binary

COPY --chown=postgres:postgres ./initialize/items.sql /docker-entrypoint-initdb.d/items.sql
# ADD https://cdn.intra.42.fr/document/document/25745/subject.zip .

# RUN unzip subject.zip 

# ADD --chown=postgres:postgres https://cdn.intra.42.fr/document/document/17535/data_2023_feb.csv   /subject/customer/

# COPY --chown=postgres:postgres ./automatic_table.sh .
# COPY --chown=postgres:postgres ./automatic_table.py .
# CMD python3 automatic_table.py