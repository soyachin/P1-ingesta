import os, psycopg2, boto3

import pandas as pd

connection = psycopg2.connect(
    database=os.getenv('PG_DB'),
    user=os.getenv('PG_USER'),
    password=os.getenv('PG_PASSWORD'),
    host=os.getenv('PG_HOST'),
    port=os.getenv('PG_PORT')
)

table_name = os.getenv('PG_TABLE')

query = 'SELECT * FROM ' + table_name

df = pd.read_sql_query(query, connection)

file = "dump_posgresql.csv"

df.to_csv(file, index=False)
print(f"Exportado a '{file}' !")

s3_client = boto3.client('s3')
bucket_name = os.getenv('S3_BUCKET')

s3_file_name = 'doctores.csv'

s3_client.upload_file('dump_postgresql.csv', bucket_name, s3_file_name)
