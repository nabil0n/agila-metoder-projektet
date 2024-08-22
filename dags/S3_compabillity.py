from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from ..src import newsfeed
import boto3
import logging
from datetime import timedelta

# connection = newsfeed.data_warehouse.database_utils.create_connection

S3_BUCKET = Variable.get("S3_BUCKET", "my_local_bucket")
S3_PREFIX = Variable.get("S3_PREFIX", "data_lake/")
LOCALSTACK_ENDPOINT = Variable.get("LOCALSTACK_ENDPOINT", "http://localhost:4566")

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=LOCALSTACK_ENDPOINT,
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="eu-north-1",
    )

def create_local_bucket(**kwargs):
    s3_client = get_s3_client()
    try:
        s3_client.create_bucket(Bucket=S3_BUCKET)
        logging.info(f"Bucket '{S3_BUCKET}' created successfully")
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        logging.info(f"Bucket '{S3_BUCKET}' already exists")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise


def upload_blog_text(**kawrgs):
    s3_client = get_s3_client()
    articles = load_articles()

    s3_urls = []
    for article in articles:
           if article.blog_text and not article.s3_url:
               try:
                   s3_key = f"{S3_PREFIX}{article.unique_id}.txt"
                   s3_client.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=article.blog_text.encode('utf-8'))
                   s3_url = f"{LOCALSTACK_ENDPOINT}/{S3_BUCKET}/{s3_key}"
                   s3_urls.append((article.unique_id, s3_url))
                   logging.info(f"Uploaded article {article.unique_id} to LocalStack S3")
               except Exception as e:
                   logging.error(f"Error uploading article {article.unique_id}: {str(e)}")

    return s3_urls

def update_database(**kwargs):
    connection, cursor = create_connection()
    try:
        ti = kwargs['ti']
        s3_urls = ti.xcom_pull(task_ids='upload_to_s3')
        
        if not s3_urls:
            logging.info("No S3 URLs to update")
            return

        update_query = """
        UPDATE iths.articles
        SET s3_url = %s
        WHERE unique_id = %s
        """
        cursor.executemany(update_query, s3_urls)
        connection.commit()
        logging.info(f"Updated {len(s3_urls)} articles with S3 URLs")
    except Exception as e:
        logging.error(f"Error updating database: {str(e)}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

defualt_args = {
    'start_date': days_ago(1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    's3_compatibility',
    default_args=defualt_args,
    schedule_interval='@daily',
    catchup=False
) as dag:
    
    create_bucket = PythonOperator(
        task_id='create_bucket',
        python_callable=create_local_bucket
    )

    upload_to_s3 = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_blog_text
    )

    update_database = PythonOperator(
        task_id='update_database',
        python_callable=update_database
    )

    create_bucket >> upload_to_s3 >> update_database

