FROM apache/airflow:latest-python3.12

COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

CMD curl http://localhost:4566
