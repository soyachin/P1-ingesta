import os, psycopg2, boto3

import pandas as pd

required_env_vars = ['PG_DB', 'PG_USER', 'PG_PASSWORD', 'PG_HOST', 'PG_PORT', 'PG_TABLE', 'S3_BUCKET']
for var in required_env_vars:
    if not os.getenv(var):
        raise EnvironmentError(f"Required environment variable {var} is not set")

try:
    connection = psycopg2.connect(
        database=os.getenv('PG_DB'),
        user=os.getenv('PG_USER'),
        password=os.getenv('PG_PASSWORD'),
        host=os.getenv('PG_HOST'),
        port=os.getenv('PG_PORT')
    )
    print("Connection to PostgreSQL DB successful")
except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL DB: {e}")
    connection = None

if connection:
    try:
        table_name = os.getenv('PG_TABLES').split(",")
        s3_client = boto3.client('s3')
        bucket_name = os.getenv('S3_BUCKET')

        for table in table_name:
            query = 'SELECT * FROM ' + table
            df = pd.read_sql(query, con=connection)
            file_name = table + '_dump.csv'
            df.to_csv(file_name, index=False)
            s3_file_name = "ing_doctores/" + table + '.csv'
            s3_client.upload_file(file_name, bucket_name, s3_file_name)
            print(f"Exported and '{file_name}' to '{bucket_name}'")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()
        print("PostgreSQL connection is closed")