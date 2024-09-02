FROM apache/airflow:latest

COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt


# RUN pip install poetry==1.8.3
# RUN pip install poetry-plugin-export

# testing updating poetry
# RUN poetry self update

# COPY pyproject.toml .

# RUN poetry init

# RUN poetry lock

# COPY poetry.lock .

# RUN poetry export --without-hashes -f requirements.txt -o requirements.txt

# RUN more requirements.txt
