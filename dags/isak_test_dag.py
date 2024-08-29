from airflow.decorators import dag, task
from airflow.sensors.time_sensor import TimeSensor
import pendulum
from newsfeed import download_blogs_from_rss, extract_articles, summarize, send_to_discord

blog_name = "mit"

@dag(
    dag_id="isak_test_dag",
    start_date=pendulum.datetime(2024, 1, 1),
    schedule="@once",
    catchup=False,
    tags=["IsakTestDag"],
    doc_md=__doc__,
    default_args={"owner": "Isak", "retries": 0},
)

def tesing_functions():
    
    @task()
    def run_newsfeed():
        download_blogs_from_rss.main(blog_name)
        extract_articles.main(blog_name)
        # return pendulum.now()
    
    @task()
    def summarize_articles():
        summarize.main(blog_name, "default")
        # return pendulum.now()
    
    @task()
    def send():
        send_to_discord.main(blog_name)
        # return pendulum.now()
    
    # run_newsfeed()
    # summarize_articles()
    # send()
    
    first_task_done = run_newsfeed()
    second_task_done = summarize_articles()
    third_task_done = send()
    
    first_task_done >> second_task_done >> third_task_done
    
tesing_functions()