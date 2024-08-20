from pathlib import Path

import jsonargparse
import requests
from loguru import logger

from newsfeed import log_utils

LINK_TO_XML_FILE = {
    "mit": "https://news.mit.edu/rss/topic/artificial-intelligence2",
}


def get_metadata_info(blog_name: str) -> str:
    assert (
        blog_name in LINK_TO_XML_FILE
    ), f"{blog_name=} not supported. Supported blogs: {list(LINK_TO_XML_FILE)}"
    blog_url = LINK_TO_XML_FILE[blog_name]
    response = requests.get(blog_url)
    xml_text = response.text
    return xml_text


def save_metadata_info(xml_text: str, blog_name: str) -> None:
    path_xml_dir = Path("data/data_lake") / blog_name
    path_xml_dir.mkdir(exist_ok=True, parents=True)
    with open(path_xml_dir / "metadata.xml", "w") as f:
        f.write(xml_text)


def main(blog_name: str) -> None:
    logger.info(f"Processing {blog_name}")
    xml_text = get_metadata_info(blog_name)
    save_metadata_info(xml_text, blog_name)
    logger.info(f"Done processing {blog_name}")


def parse_args() -> jsonargparse.Namespace:
    parser = jsonargparse.ArgumentParser()
    parser.add_function_arguments(main)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    log_utils.configure_logger(log_level="DEBUG")
    main(**args)
