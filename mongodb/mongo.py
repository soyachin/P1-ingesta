import json, boto3
from pymongo import MongoClient
import os
from datetime import datetime

def convert_datetime(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')

required_env_vars = ['MONGO_CLIENT', 'S3_BUCKET']
for var in required_env_vars:
    if not os.getenv(var):
        raise EnvironmentError(f"Required environment variable {var} is not set")

try:
    mongo_client = MongoClient(os.getenv('MONGO_CLIENT'))
    db = mongo_client['P1pacientes_test']
    collection = db['Pacientes']
    print("Connection to MongoDB successful")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    mongo_client = None

if mongo_client:
    datos = list(collection.find())

    with open('ingesta_pacientes.json', 'w') as outfile:
        json.dump(datos, outfile, default=convert_datetime, indent=4)

    s3_client = boto3.client('s3')
    bucket_name = os.getenv('S3_BUCKET')

    s3_file_name = 'ing_pacientes/pacientes.json'

    s3_client.upload_file('ingesta_pacientes.json', bucket_name, s3_file_name)
    print(f"Exported to '{s3_file_name}'!")
