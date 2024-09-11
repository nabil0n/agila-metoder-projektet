from datetime import timedelta

import pendulum
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from S3_utils import (
    create_local_bucket,
    initialize_database,
    update_database_with_s3_urls,
    upload_blog_text,
)

default_args = {
    "start_date": days_ago(1),
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "owner": "Grupp2",
}


@dag(
    dag_id="s3_compatibility",
    start_date=days_ago(1),
    schedule="@once",
    catchup=False,
    tags=["s3"],
    doc_md=__doc__,
    default_args={"owner": "Grupp2", "retries": 0},
)
def s3_bucket_init():

    @task()
    def create_bucket():
        create_local_bucket()
        return pendulum.now()

    @task()
    def upload_to_s3():
        upload_blog_text()
        return pendulum.now()

    @task()
    def initialize_db():
        initialize_database()
        return pendulum.now()

    @task()
    def update_database_dag():
        update_database_with_s3_urls()
        return pendulum.now()

    first = create_bucket()
    second = upload_to_s3()
    third = initialize_db()
    fourth = update_database_dag()

    first >> second >> third >> fourth


s3_bucket_init()
