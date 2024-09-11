import pendulum
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

from newsfeed import (
    clearbucket,
    download_blogs_from_rss,
    extract_articles,
    send_to_discord,
    summarize,
)

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
    """
    This function defines a DAG (Directed Acyclic Graph) for a pipeline process. It consists of several tasks that are executed sequentially.
    Tasks:
    - run_newsfeed: Downloads blogs from an RSS feed and extracts articles.
    - summarize_articles: Summarizes the extracted articles.
    - send_webhook: Sends the summarized articles to Discord.
    - clear_bucket: Clears a bucket.
    Execution Flow:
    1. run_newsfeed task is executed.
    2. summarize_articles task is executed.
    3. send_webhook task is executed.
    4. clear_bucket task is executed.
    Returns:
    - The current timestamp when each task is completed.
    """

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

    first >> second >> third >> fourth

tesing_functions()
