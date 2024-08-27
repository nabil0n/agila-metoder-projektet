import jsonargparse
from loguru import logger

from newsfeed import extract_articles, log_utils
from newsfeed.data_warehouse import database_utils
from newsfeed.datatypes import BlogInfo


def main(blog_name: str) -> None:
    logger.info(f"Processing {blog_name}")
    parsed_xml = extract_articles.load_metadata(blog_name)
    articles = extract_articles.extract_articles_from_xml(parsed_xml)
    save_articles_data_warehouse(articles)
    logger.info(f"Done processing {blog_name}")


def save_articles_data_warehouse(articles: list[BlogInfo]) -> None:
    database_utils.delete_articles_table()
    database_utils.create_articles_table()
    database_utils.add_articles(articles)


def parse_args() -> jsonargparse.Namespace:
    parser = jsonargparse.ArgumentParser()
    parser.add_function_arguments(main)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    log_utils.configure_logger(log_level="DEBUG")
    main(**args)
