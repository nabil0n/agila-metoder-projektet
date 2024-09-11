from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import pendulum
from newsfeed import download_blogs_from_rss, extract_articles, summarize, send_to_discord, clearbucket

blog_name = "mit"

@dag(
    dag_id="newspipeline",
    start_date=days_ago(1),
    schedule="@daily",
    catchup=False,
    tags=["newsfeed"],
    doc_md=__doc__,
    default_args={"owner": "Grupp2", "retries": 0},
)

def tesing_functions():
    
    @task()
    def run_newsfeed():
        download_blogs_from_rss.main(blog_name)
        extract_articles.main(blog_name)
        return pendulum.now()
    
    @task()
    def summarize_articles():
        summarize.main(blog_name, "non_technical")
        return pendulum.now()
    
    @task()
    def send_webhook():
        send_to_discord.main(blog_name)
        return pendulum.now()
    
    @task()
    def clear_bucket():
        clearbucket.main()
        return pendulum.now()
    
    first = run_newsfeed()
    second = summarize_articles()
    third = send_webhook()
    fourth = clear_bucket()
    
    first >> second  >> third >> fourth
    
tesing_functions()