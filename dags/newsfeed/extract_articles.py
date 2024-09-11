import uuid
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup
from loguru import logger
from newsfeed.datatypes import BlogInfo
from S3_utils import get_s3_client

from newsfeed import log_utils

s3_client = get_s3_client()

S3_BUCKET = "my-local-bucket"
S3_PREFIX = "data_lake/"
LOCALSTACK_ENDPOINT = "http://localhost:4566"
WAREHOUSE_PREFIX = "data_warehouse/"


def create_uuid_from_string(val: str) -> str:
    assert isinstance(val, str)
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, val))


def load_metadata_info_to_s3(blog_name: str) -> BeautifulSoup:
    s3_key = f"{S3_PREFIX}{blog_name}/metadata.xml"

    try:
        xml_text = s3_client.get_object(Bucket=S3_BUCKET, Key=s3_key)["Body"]
        logger.info(f"Downloaded metadata for {blog_name} from Localstack S3: {s3_key}")
        parsed_xml = BeautifulSoup(xml_text, "xml")
        return parsed_xml

    except Exception as e:
        logger.error(f"Failed to download metadata for {blog_name}: {str(e)}")
        raise


def extract_articles_from_xml(parsed_xml: BeautifulSoup) -> list[BlogInfo]:
    articles = []
    for item in parsed_xml.find_all("item"):
        logger.debug(f"Processing {item.title.text}")
        raw_blog_text = (
            item.find("content:encoded").text
            if item.find("content:encoded")
            else item.find("description").text
        )
        soup = BeautifulSoup(raw_blog_text, "html.parser")
        blog_text = soup.get_text()
        title = item.title.text

        title = title.replace("\n", "")
        logger.debug(f"{title=}")

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

    for article in articles:
        s3_key = f"{WAREHOUSE_PREFIX}{blog_name}/articles/{article.filename}"
        try:
            s3_client.put_object(
                Bucket=S3_BUCKET, Key=s3_key, Body=article.to_json().encode("utf-8")
            )
            logger.info(f"Saved article {article.filename} to S3 at {s3_key}")
        except Exception as e:
            logger.error(f"Failed to save article {article.filename} to S3 at {s3_key}: {str(e)}")
            continue


def main(blog_name: str) -> None:
    logger.info(f"Processing {blog_name}")
    parsed_xml = load_metadata_info_to_s3(blog_name)
    articles = extract_articles_from_xml(parsed_xml)
    save_articles(articles, blog_name)
    logger.info(f"Done processing {blog_name}")
    log_utils.configure_logger(log_level="DEBUG")
