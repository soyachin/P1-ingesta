import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host = 'HOST',
    user = "MYSQL_USER",
    password = "MYSQL_PASSWORD",
    database = 'MYSQL_DB'
)

table_name = 'MYSQL_TABLE'

query = 'SELECT * FROM' + table_name

df = pd.read_sql(query, con=mydb)

file = 'dump.csv'
df.to_csv(file, index=False)
print(f"Exportado a '{file}' !")



