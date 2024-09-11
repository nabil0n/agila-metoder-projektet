import requests
from loguru import logger
from S3_utils import get_s3_client

from newsfeed import log_utils

s3_client = get_s3_client()

LINK_TO_XML_FILE = {
    "mit": "https://news.mit.edu/rss/topic/artificial-intelligence2",
    "bbc": "http://feeds.bbci.co.uk/news/world/rss.xml",  # FUNKAR! Men bara på redan sammanfattad text
    "uneu": "https://news.un.org/feed/subscribe/en/news/region/europe/feed/rss.xml",  # FUNKAR! Men bara på redan sammanfattad text
    "jmlr": "https://www.jmlr.org/jmlr.xml",  # FUNKAR! Men bara på redan sammanfattad text
}

S3_BUCKET = "my-local-bucket"
S3_PREFIX = "data_lake/"
LOCALSTACK_ENDPOINT = "http://localhost:4566"


def get_metadata_info(blog_name: str) -> str:
    """
    Retrieves the metadata information of a blog.

    Args:
        blog_name (str): The name of the blog.

    Returns:
        str: The XML text containing the metadata information of the blog.

    Raises:
        AssertionError: If the specified blog name is not supported.

    """
    assert (
        blog_name in LINK_TO_XML_FILE
    ), f"{blog_name=} not supported. Supported blogs: {list(LINK_TO_XML_FILE)}"
    blog_url = LINK_TO_XML_FILE[blog_name]
    response = requests.get(blog_url)
    xml_text = response.text
    return xml_text


def save_metadata_info_to_s3(xml_text: str, blog_name: str) -> None:
    """
    Saves the metadata information to S3.
    Args:
        xml_text (str): The XML text containing the metadata information.
        blog_name (str): The name of the blog.
    Returns:
        None
    """
    s3_key = f"{S3_PREFIX}{blog_name}/metadata.xml"

    try:
        s3_client.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=xml_text.encode("utf-8"))
        logger.info(f"Updloaded metadata for {blog_name} to Localstack S3: {s3_key}")
    except Exception as e:
        logger.error(f"Failed to upload metadata for {blog_name} to Localstack S3: {s3_key}")
        logger.error(e)


def main(blog_name: str) -> None:
    logger.info(f"Processing {blog_name}")
    xml_text = get_metadata_info(blog_name)
    save_metadata_info_to_s3(xml_text, blog_name)
    save_metadata_info_to_s3(xml_text, blog_name)
    logger.info(f"Done processing {blog_name}")
    log_utils.configure_logger(log_level="DEBUG")
