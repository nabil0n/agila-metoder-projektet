from airflow.decorators import dag, task
from pendulum import datetime
from newsfeed import download_blogs_from_rss, extract_articles, summarize


@dag(
    dag_id="isak_test_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@once",
    catchup=False,
    tags=["IsakTestDag"],
    doc_md=__doc__,
    default_args={"owner": "Isak", "retries": 0},
)

def tesing_functions():
    
    @task()
    def run_newsfeed():
        download_blogs_from_rss.main("mit")
        extract_articles.main("mit")
    
    run_newsfeed()
    
    @task()
    def summarize_articles():
        summarize.main("mit", "default")
    
    summarize_articles()
    
tesing_functions()