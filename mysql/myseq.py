import os

import mysql.connector
from mysql.connector import Error
import pandas as pd
import boto3

required_env_vars = ['MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DATABASE', 'MYSQL_PORT', 'MYSQL_TABLE', 'S3_BUCKET']
for var in required_env_vars:
    if not os.getenv(var):
        raise EnvironmentError(f"Required environment variable {var} is not set")


try:
    mydb = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE'),
        port=os.getenv('MYSQL_PORT')
    )

    if mydb.is_connected():
        table_name = os.getenv('MYSQL_TABLE')
        query = 'SELECT * FROM ' + table_name

        df = pd.read_sql(query, con=mydb)

        file = 'dump_mysql.csv'
        df.to_csv(file, index=False)

        s3_client = boto3.client('s3')
        bucket_name = os.getenv('S3_BUCKET')

        s3_file_name = 'historia_medica.csv'
        s3_client.upload_file('dump_mysql.csv', bucket_name, s3_file_name)

except Error as e:
    print(f"Error connecting to MySQL: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if 'mydb' in locals() and mydb.is_connected():
        mydb.close()
        print("MySQL connection is closed")