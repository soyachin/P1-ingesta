import os

import mysql.connector
import pandas as pd
import boto3

mydb = mysql.connector.connect(
    host = os.getenv('MYSQL_HOST'),
    user = os.getenv('MYSQL_USER'),
    password = os.getenv('MYSQL_PASSWORD'),
    database = os.getenv('MYSQL_DATABASE')
)

table_name = os.getenv('MYSQL_TABLE')

query = 'SELECT * FROM ' + table_name

df = pd.read_sql(query, con=mydb)

file = 'dump_mysql.csv'
df.to_csv(file, index=False)

s3_client = boto3.client('s3')
bucket_name = os.getenv('S3_BUCKET')

s3_file_name = 'historia_medica.csv'

s3_client.upload_file('dump_mysql.csv', bucket_name, s3_file_name)
