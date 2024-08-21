FROM apache/airflow:latest

RUN pip install poetry==1.8.3
RUN pip install poetry-plugin-export

# adding manual install of setupttols
# RUN pip install --upgrade setuptools

# testing updating poetry
RUN poetry self update

COPY pyproject.toml .

# re-lock poetry.lock
RUN poetry lock

COPY poetry.lock .

RUN poetry export --without-hashes -f requirements.txt -o requirements.txt

# testing adding numpy version here
# RUN pip install numpy==1.26.4

RUN pip install -r requirements.txt

# RUN more requirements.txt
