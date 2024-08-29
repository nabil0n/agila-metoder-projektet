from pathlib import Path

import jsonargparse
import pydantic
from discord import SyncWebhook
from loguru import logger

from newsfeed import log_utils
from newsfeed.datatypes import BlogSummary


def load_summaries(blog_name: str) -> list[BlogSummary]:
    logger.debug(f"Processing {blog_name}")

    summaries = []
    save_dir = Path("data/datasets", blog_name, "summaries")
    for summary_file in save_dir.glob("**/*.json"):
        summary = pydantic.parse_file_as(BlogSummary, summary_file)
        # logger.debug(summary)
        summaries.append(summary)

    return summaries


def send_to_discord(summary: BlogSummary) -> None:
    discord_webhook_url = "<your webhook here>"
    webhook = SyncWebhook.from_url(discord_webhook_url)

    group_name = "<NoName>"
    message = f"**Group name: {group_name}**\n**{summary.title}**\n```{summary.text}```"
    webhook.send(message)


def main(blog_name: str) -> None:
    logger.debug(f"Processing {blog_name}")
    summaries = load_summaries(blog_name)

    for summary in summaries:
        send_to_discord(summary)


def parse_args() -> jsonargparse.Namespace:
    parser = jsonargparse.ArgumentParser()
    parser.add_function_arguments(main)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    log_utils.configure_logger(log_level="DEBUG")
    main(**args)
