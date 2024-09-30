import psycopg2

con = psycopg2.connect(
    dbname="piscineds",
    user="alorain",
    host="localhost",
    password="mysecretpassword",
)
with con.cursor() as cursor:
    with open("customers_table.sql", "r") as sql_file:
        cursor.execute(sql_file.read())
    con.commit()
    con.close()
    cursor.close()
