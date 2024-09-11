from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from newsfeed.data_warehouse.database_utils import create_connection, load_articles, create_articles_table
import boto3
from loguru import logger
from datetime import timedelta


S3_BUCKET = "my-local-bucket"
S3_PREFIX = "data-lake/"
LOCALSTACK_ENDPOINT = "http://localstack:4566"

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=LOCALSTACK_ENDPOINT,
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
    )

s3_client = get_s3_client()

def initialize_database(**kwargs):
    create_articles_table()
    logger.info("Database initialized")

def create_local_bucket(**kwargs):
    try:
        s3_client.create_bucket(Bucket=S3_BUCKET)
        logger.info(f"Bucket '{S3_BUCKET}' created successfully")
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        logger.info(f"Bucket '{S3_BUCKET}' already exists")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise


def upload_blog_text(**kwargs):
    articles = load_articles()

    s3_urls = []
    for article in articles:
            if article.blog_text and not article.s3_url:
                try:
                    s3_key = f"{S3_PREFIX}{article.unique_id}.txt"
                    s3_client.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=article.blog_text.encode('utf-8'))
                    s3_url = f"{LOCALSTACK_ENDPOINT}/{S3_BUCKET}/{s3_key}"
                    s3_urls.append((article.unique_id, s3_url))
                    logger.info(f"Uploaded article {article.unique_id} to LocalStack S3")
                except Exception as e:
                    logger.error(f"Error uploading article {article.unique_id}: {str(e)}")

    return s3_urls

def update_database_with_s3_urls(**kwargs):
    connection, cursor = create_connection()
    try:
        ti = kwargs['ti']
        s3_urls = ti.xcom_pull(task_ids='upload_to_s3')
        
        if not s3_urls:
            logger.info("No S3 URLs to update")
            return

        update_query = """
        UPDATE iths.articles
        SET s3_url = %s
        WHERE unique_id = %s
        """
        cursor.executemany(update_query, s3_urls)
        connection.commit()
        logger.info(f"Updated {len(s3_urls)} articles with S3 URLs")
    except Exception as e:
        logger.error(f"Error updating database: {str(e)}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

default_args = {
    'start_date': days_ago(1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'owner': 'Grupp2',
}

@dag(
    dag_id='s3_compatibility',
    default_args=default_args,
    schedule="@once",
    catchup=False,
    doc_md=__doc__,
)

def s3_bucket_init():
    
    @task()
    def create_bucket():
        create_local_bucket()
    
    @task()
    def upload_to_s3():
        upload_blog_text()
    
    @task()
    def initialize_db():
        initialize_database()
    
    @task()
    def update_database_dag():
        update_database_with_s3_urls()
    
    first = create_bucket()
    second = upload_to_s3()
    third = initialize_db()
    fourth = update_database_dag()
    
    first >> second >> third >> fourth

s3_bucket_init()