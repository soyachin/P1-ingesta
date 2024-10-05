import json, boto3
from pymongo import MongoClient
import os

mongo_client = MongoClient(os.getenv('MONGO_CLIENT'))
db = mongo_client['P1pacientes_test']
collection = db['Pacientes']

datos = list(collection.find())

with open('ingesta_pacientes.json', 'w') as outfile:
    json.dump(datos, outfile)

s3_client = boto3.client('s3')
bucket_name = os.getenv('S3_BUCKET')

s3_file_name = 'pacientes.json'

s3_client.upload_file('ingesta_pacientes.json', bucket_name, s3_file_name)

