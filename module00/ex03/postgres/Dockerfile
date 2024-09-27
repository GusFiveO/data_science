FROM postgres:16

RUN apt update && apt install unzip

COPY --chown=postgres:postgres ./generate_tables.sh .
ADD https://cdn.intra.42.fr/document/document/25745/subject.zip .

RUN unzip subject.zip
RUN ./generate_tables.sh
