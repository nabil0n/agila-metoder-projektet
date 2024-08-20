SHELL := /bin/bash

install_dependencies:
	poetry config virtualenvs.in-project true
	poetry lock --no-update
	poetry install --sync
	poetry run pre-commit install --hook-type pre-push --hook-type post-checkout --hook-type pre-commit

run_precommit:
	poetry run pre-commit run --all-files

run_tests:
	poetry run pytest tests/

build_docker:
	docker-compose build

start_airflow:
	docker-compose up
