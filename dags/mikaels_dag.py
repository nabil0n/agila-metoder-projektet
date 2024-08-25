from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from newsfeed.download_blogs_from_rss import get_metadata_info
from newsfeed.extract_articles import extract_articles_from_xml
from newsfeed.data_warehouse.save_articles import save_articles_data_warehouse
from newsfeed.summarize import create_summaries
from newsfeed.send_to_discord import send_to_discord as send_discord_message

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'retries': 1,
}

dag = DAG(
    'newsfeed_processing_dag',
    default_args=default_args,
    description='A DAG to process news feeds, summarize articles, and push to Discord',
    schedule_interval='@daily',
)

# Task 1: Download RSS feeds
def download_blogs(**kwargs):
    blog_name = kwargs['blog_name']
    metadata_info = get_metadata_info(blog_name)
    kwargs['ti'].xcom_push(key='metadata_info', value=metadata_info)

download_blogs_task = PythonOperator(
    task_id='download_blogs_task',
    python_callable=download_blogs,
    op_kwargs={'blog_name': 'mit'},
    dag=dag,
)

# Task 2: Extract articles from the feeds
def extract_articles(**kwargs):
    blog_name = kwargs['blog_name']
    metadata_info = kwargs['ti'].xcom_pull(key='metadata_info', task_ids='download_blogs_task')
    articles = extract_articles_from_xml(metadata_info)
    kwargs['ti'].xcom_push(key='articles', value=articles)

extract_articles_task = PythonOperator(
    task_id='extract_articles_task',
    python_callable=extract_articles,
    op_kwargs={'blog_name': 'mit'},
    dag=dag,
)

# Task 3: Save the extracted articles to the database
def save_articles(**kwargs):
    articles = kwargs['ti'].xcom_pull(key='articles', task_ids='extract_articles_task')
    save_articles_data_warehouse(articles)

save_articles_task = PythonOperator(
    task_id='save_articles_task',
    python_callable=save_articles,
    dag=dag,
)

# Task 4: Summarize the articles
def summarize_articles(**kwargs):
    create_summaries(summary_type="default")

summarize_articles_task = PythonOperator(
    task_id='summarize_articles_task',
    python_callable=summarize_articles,
    dag=dag,
)

# Task 5: Send summaries to Discord
def send_to_discord(**kwargs):
    send_discord_message()

send_to_discord_task = PythonOperator(
    task_id='send_to_discord_task',
    python_callable=send_to_discord,
    dag=dag,
)

# Set task dependencies
download_blogs_task >> extract_articles_task >> save_articles_task >> summarize_articles_task >> send_to_discord_task
