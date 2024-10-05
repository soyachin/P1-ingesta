FROM python:3.9-slim

WORKDIR /ingesta

RUN pip3 install boto3 mysql-connector pandas

COPY .. .

CMD ["python3", "mysql/myseq.py"]