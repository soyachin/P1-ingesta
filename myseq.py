import os

import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host = os.getenv('MYSQL_HOST'),
    user = os.getenv('MYSQL_USER'),
    password = os.getenv('MYSQL_PASSWORD'),
    database = os.getenv('MYSQL_DATABASE')
)

table_name = 'MYSQL_TABLE'

query = 'SELECT * FROM' + table_name

df = pd.read_sql(query, con=mydb)

file = 'dump.csv'
df.to_csv(file, index=False)
print(f"Exportado a '{file}' !")



