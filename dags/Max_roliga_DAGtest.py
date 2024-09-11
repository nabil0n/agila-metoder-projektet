import pendulum 
from airflow.decorators import dag, task
from newsfeed import download_blogs_from_rss, extract_articles, send_to_discord, summarize
blog_name = "mit"

@dag(
    dag_id="max_dag_test",
    start_date=pendulum.datetime(2024, 8, 31),
    schedule="*/1 * * * *",
    catchup=False,
)

def task_functions():

    @task(task_id="summarizes")
    def summarizes():
        summarize.main(blog_name)

    @task(task_id="download_extract")
    def download_extract():
        extract_articles.main(blog_name)
        download_blogs_from_rss.main(blog_name)

    @task(task_id="discord")
    def discord_send():
        send_to_discord.main(blog_name)

    # def test_pipelines():
    #     download_extract()
    #     summarizes()
    #     discord_send()

    #     test_pipelines()
    

    task_one = download_extract()
    task_two = summarizes()
    task_three = discord_send()

    task_one >> task_two >> task_three
