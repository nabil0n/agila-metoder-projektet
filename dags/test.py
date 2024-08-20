from datetime import datetime

from airflow.decorators import dag, task

from newsfeed import dag_start, download_blogs_from_rss


@task(task_id="hello")
def hello_task() -> None:
    print("HELLO suuup")
    print(dag_start.get_name())


@task(task_id="download_blogs_from_rss")
def download_blogs_from_rss_task() -> None:
    download_blogs_from_rss.main(blog_name="mit")


@dag(
    dag_id="test_pipeline",
    start_date=datetime(2023, 6, 2),
    schedule="*/5 * * * *",
    catchup=False,
)
def test_pipeline() -> None:
    # hello_task() >> download_blogs_from_rss_task()
    hello_task()
    download_blogs_from_rss_task()


# register DAG
test_pipeline()
