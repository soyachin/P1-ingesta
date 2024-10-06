FROM python:3.9-slim

WORKDIR /ingesta

RUN pip3 install boto3 psycopg2-binary pandas

COPY . .

CMD ["python3", "postgres.py"]