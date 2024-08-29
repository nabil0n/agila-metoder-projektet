import uuid
from datetime import datetime
from pathlib import Path

import jsonargparse
import pandas as pd
from bs4 import BeautifulSoup
from loguru import logger

from newsfeed import log_utils
from newsfeed.datatypes import BlogInfo


def create_uuid_from_string(val: str) -> str:
    assert isinstance(val, str)
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, val))


def load_metadata(blog_name: str) -> BeautifulSoup:
    metadata_path = Path("data/data_lake") / blog_name / "metadata.xml"
    with open(metadata_path) as f:
        xml_text = f.read()

    parsed_xml = BeautifulSoup(xml_text, "xml")
    return parsed_xml


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
    save_dir = Path("data/data_warehouse", blog_name, "articles")
    save_dir.mkdir(exist_ok=True, parents=True)
    for article in articles:
        save_path = save_dir / article.filename
        with open(save_path, "w") as f:
            f.write(article.json(indent=2))


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
