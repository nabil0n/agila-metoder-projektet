from datetime import datetime

from airflow.decorators import dag, task

from src import newsfeed


@task(task_id="hello")
def hello_task() -> None:
    print("HELLO suuup")
    print(newsfeed.dag_start.get_name())


@task(task_id="download_blogs_from_rss")
def download_blogs_from_rss_task() -> None:
    newsfeed.download_blogs_from_rss.main(blog_name="mit")


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
