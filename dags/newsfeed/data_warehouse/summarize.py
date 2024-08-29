import dotenv
import jsonargparse
from loguru import logger

from newsfeed import log_utils, summarize
from newsfeed.data_warehouse import database_utils


def main(blog_name: str) -> None:
    logger.info(f"Processing {blog_name}")
    articles = database_utils.load_articles()
    summarize.create_summaries(articles, summary_type="default")
    logger.info(f"Done processing {blog_name}")


def parse_args() -> jsonargparse.Namespace:
    parser = jsonargparse.ArgumentParser()
    parser.add_function_arguments(main)
    return parser.parse_args()


if __name__ == "__main__":
    dotenv.load_dotenv("cfg/dev.env")
    args = parse_args()
    log_utils.configure_logger(log_level="DEBUG")
    main(**args)
