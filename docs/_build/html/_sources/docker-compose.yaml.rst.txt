Docker Compose Configuration for Airflow
========================================

This `docker-compose.yaml` file sets up a basic Airflow cluster configuration using `CeleryExecutor`, `Redis`, and `PostgreSQL` for local development purposes. This setup is **not** recommended for production use.

.. warning::
   This configuration is for local development only. Do not use it in a production environment.

Environment Variables
---------------------

This Docker Compose configuration allows for basic customization through environment variables, or by using an `.env` file. The following variables are supported:

- **AIRFLOW_IMAGE_NAME**: Docker image name used to run Airflow. Default: `apache/airflow:2.10.0`
- **AIRFLOW_UID**: User ID in Airflow containers. Default: `50000`
- **AIRFLOW_PROJ_DIR**: Base path to which all the files will be mounted. Default: `.`
- **_AIRFLOW_WWW_USER_USERNAME**: Username for the administrator account. Default: `airflow`
- **_AIRFLOW_WWW_USER_PASSWORD**: Password for the administrator account. Default: `airflow`
- **_PIP_ADDITIONAL_REQUIREMENTS**: Additional Python packages to install at container startup. 
  This is intended only for quick checks, and it's recommended to extend the official Airflow image for custom dependencies.

.. note::
   For more robust configurations, it's better to extend the official Docker image as described in 
   the Airflow documentation: 
   https://airflow.apache.org/docs/docker-stack/build.html

Services Overview
-----------------

- **PostgreSQL**: This service uses the `postgres:13` Docker image and serves as the backend database for Airflow.
- **Redis**: The `redis:7.2-bookworm` image is used as the broker for `CeleryExecutor`.
- **Airflow Webserver**: The Airflow web interface is exposed on port `8080`.
- **Airflow Scheduler**: Handles task scheduling and runs health checks on port `8974`.
- **Airflow Worker**: The worker node for running tasks with the `CeleryExecutor`.
- **Airflow Triggerer**: The triggerer service is used to handle deferred tasks.
- **Localstack**: Used for mocking AWS services such as S3. Exposed on ports `4566` and `4571`.
- **Airflow Init**: Initializes the Airflow environment, creating the necessary user accounts and databases.
- **Flower (optional)**: This service provides a web-based UI for monitoring Celery jobs, exposed on port `5555`.

PostgreSQL Service
------------------
- **Image**: `postgres:13`
- **Environment Variables**:
  - `POSTGRES_USER`: The username for PostgreSQL (default: `airflow`).
  - `POSTGRES_PASSWORD`: The password for PostgreSQL (default: `airflow`).
  - `POSTGRES_DB`: The database name (default: `airflow`).
- **Volumes**: Persists PostgreSQL data to the `postgres-db-volume` volume.
- **Health Check**: Uses the `pg_isready` command to check database availability.

Redis Service
-------------
- **Image**: `redis:7.2-bookworm`
- **Ports**: Exposes port `6379` for Redis communication.
- **Health Check**: Uses the `redis-cli ping` command to check if Redis is ready.

Airflow Webserver
-----------------
- **Command**: `webserver`
- **Ports**: Exposes the Airflow UI on port `8080`.
- **Health Check**: Uses a simple `curl` command to check the health of the webserver by pinging `/health`.

Airflow Scheduler
-----------------
- **Command**: `scheduler`
- **Health Check**: Runs on port `8974` for health monitoring.
- **Dependencies**: Depends on both Redis and PostgreSQL services to be healthy before starting.

Airflow Worker
--------------
- **Command**: `celery worker`
- **Health Check**: Runs a Celery ping command to verify the worker is alive and responsive.
- **Environment Variables**: Includes special configuration for `DUMB_INIT_SETSID` to ensure proper shutdown handling.

Airflow Triggerer
-----------------
- **Command**: `triggerer`
- **Health Check**: Uses the Airflow command `airflow jobs check` to verify the TriggererJob is running correctly.

Localstack
----------
- **Image**: `localstack/localstack`
- **Environment Variables**:
  - `SERVICES`: Specifies which AWS services to mock (default: `s3`).
  - `DEBUG`: Enables debug mode.
- **Ports**: Exposes ports `4566` and `4571` for Localstack communication.

.. note::
   Localstack is used to mock AWS services like S3 for testing purposes.

Airflow Init Service
--------------------
This service is responsible for initializing the Airflow environment, including:
- Database migrations.
- Creating the default Airflow admin user.
- Setting permissions on directories.

.. note::
   Make sure to check the warnings regarding insufficient resources (memory, CPU, and disk space) that are printed during initialization.

Volumes
-------

The following volumes are defined in this configuration:

- `postgres-db-volume`: Stores PostgreSQL database files.
- `localstack-data`: Stores Localstack data.
- Various project directories, such as `dags`, `logs`, `plugins`, `config`, `data`, and `src/newsfeed` are mounted to specific paths in the Airflow containers.

Additional Notes
----------------
- **PYTHONPATH Configuration**: The `PYTHONPATH` is customized to include `/mnt/package-code`, which allows for dynamic loading of Python code during development.
- **Health Checks**: Each major service in this configuration includes a health check, ensuring that services are ready before dependent services start.
- **Licensing**: This file is licensed under the Apache License, Version 2.0. Refer to the `LICENSE` file for more details.

References:
-----------
- `Airflow Docker Documentation`: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
