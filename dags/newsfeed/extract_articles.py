import uuid
from datetime import datetime
from pathlib import Path
import boto3
import jsonargparse
import pandas as pd
import json
import pydantic
from bs4 import BeautifulSoup
from loguru import logger

from newsfeed import log_utils
from newsfeed.datatypes import BlogInfo

from S3_compabillity import get_s3_client

S3_BUCKET = "my-local-bucket"
S3_PREFIX = "data-lake/"
LOCALSTACK_ENDPOINT = "http://localstack:4566"
WAREHOUSE_PREFIX = "data-warehouse/"


def create_uuid_from_string(val: str) -> str:
    assert isinstance(val, str)
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, val))

def load_metadata(blog_name: str) -> BeautifulSoup:
    s3_client = get_s3_client()
    s3_key = f"{S3_PREFIX}{blog_name}/metadata.xml"

    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=s3_key)
        xml_text = response['Body'].read().decode('utf-8')
        parsed_xml = BeautifulSoup(xml_text, "xml")
        return parsed_xml
    except Exception as e:
        logger.error(f"Error loading metadata from S3: {e}")
        raise

# def load_metadata(blog_name: str) -> BeautifulSoup:
#     metadata_path = Path("data/data_lake") / blog_name / "metadata.xml"
#     with open(metadata_path) as f:
#         xml_text = f.read()

#     parsed_xml = BeautifulSoup(xml_text, "xml")
#     return parsed_xml


def extract_articles_from_xml(parsed_xml: BeautifulSoup) -> list[BlogInfo]:
    articles = []
    for item in parsed_xml.find_all("item"):
        raw_blog_text = item.find("content:encoded").text
        soup = BeautifulSoup(raw_blog_text, "html.parser")
        blog_text = soup.get_text()
        title = item.title.text
        unique_id = create_uuid_from_string(title)
        article_info = BlogInfo(
            unique_id=unique_id,
            title=title,
            description=item.description.text,
            link=item.link.text,
            blog_text=blog_text,
            published=pd.to_datetime(item.pubDate.text).date(),
            timestamp=datetime.now(),
        )
        articles.append(article_info)

    return articles

def save_articles(articles: list[BlogInfo], blog_name: str) -> None:
    s3_client = get_s3_client()

    for article in articles:
        s3_key = f"{WAREHOUSE_PREFIX}{blog_name}/articles/{article.filename}"
        try:
            s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=s3_key,
                Body=article.to_json().encode('utf-8')
            )
            logger.info(f"Saved artic.e {article.unique_id} to S3 at {s3_key}")
        except Exception as e:
            logger.error(f"Error saving article {article.unique_id} to S3: {e}")
            
    
# def save_articles(articles: list[BlogInfo], blog_name: str) -> None:
#     save_dir = Path("data/data_warehouse", blog_name, "articles")
#     save_dir.mkdir(exist_ok=True, parents=True)
#     for article in articles:
#         save_path = save_dir / article.filename
#         with open(save_path, "w") as f:
#             f.write(article.to_json())


def main(blog_name: str) -> None:
    logger.info(f"Processing {blog_name}")
    parsed_xml = load_metadata(blog_name)
    articles = extract_articles_from_xml(parsed_xml)
    save_articles(articles, blog_name)
    logger.info(f"Done processing {blog_name}")


def parse_args() -> jsonargparse.Namespace:
    parser = jsonargparse.ArgumentParser()
    parser.add_function_arguments(main)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    log_utils.configure_logger(log_level="DEBUG")
    main(**args)
