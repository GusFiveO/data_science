FROM postgres:16


COPY --chown=postgres:postgres ./tables.sql /docker-entrypoint-initdb.d/tables.sql
COPY --chown=postgres:postgres ./customer /docker-entrypoint-initdb.d/customer
