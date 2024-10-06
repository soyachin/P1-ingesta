FROM python:3.9-slim

WORKDIR /ingesta

RUN pip3 install boto3 pymongo

COPY . .

CMD ["python3", "mongo.py"]