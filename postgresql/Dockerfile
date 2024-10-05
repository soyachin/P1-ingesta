FROM python:3.9-slim

WORKDIR /ingesta

RUN pip3 install boto3 psycopg2 pandas

COPY .. .

CMD ["python3", "postgresql/postgres.py"]