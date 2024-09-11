from pathlib import Path
import boto3
import jsonargparse
import requests
from loguru import logger

from newsfeed import log_utils

LINK_TO_XML_FILE = {
    "mit": "https://news.mit.edu/rss/topic/artificial-intelligence2",
}

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

def get_metadata_info(blog_name: str) -> str:
    assert (
        blog_name in LINK_TO_XML_FILE
    ), f"{blog_name=} not supported. Supported blogs: {list(LINK_TO_XML_FILE)}"
    blog_url = LINK_TO_XML_FILE[blog_name]
    response = requests.get(blog_url)
    xml_text = response.text
    return xml_text


def save_metadata_info_to_s3(xml_text: str, blog_name: str) -> None:
    s3_client = get_s3_client()
    s3_key = f"{S3_PREFIX}{blog_name}/metadata.xml"

    try:
        s3_client.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=xml_text.encode('utf-8'))
        logger.info(f"Uploaded metadata for {blog_name} to LocalStack S3: {s3_key}")
    except Exception as e:
        logger.error(f"Error uploading metadata for {blog_name}: {str(e)}")
        raise

#def save_metadata_info(xml_text: str, blog_name: str) -> None:
    #path_xml_dir = Path("data/data_lake") / blog_name
    #path_xml_dir.mkdir(exist_ok=True, parents=True)
   # with open(path_xml_dir / "metadata.xml", "w") as f:
   #     f.write(xml_text)


def main(blog_name: str) -> None:
    logger.info(f"Processing {blog_name}")
    xml_text = get_metadata_info(blog_name)
    save_metadata_info_to_s3(xml_text, blog_name)
    logger.info(f"Done processing {blog_name}")


def parse_args() -> jsonargparse.Namespace:
    parser = jsonargparse.ArgumentParser()
    parser.add_function_arguments(main)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    log_utils.configure_logger(log_level="DEBUG")
    main(**args)

