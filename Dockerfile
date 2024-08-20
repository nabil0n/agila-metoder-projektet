FROM apache/airflow:latest

RUN pip install poetry
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry export --without-hashes -f requirements.txt -o requirements.txt
RUN pip install -r requirements.txt
