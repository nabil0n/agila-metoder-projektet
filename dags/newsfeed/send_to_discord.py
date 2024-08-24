from pathlib import Path

import jsonargparse
import pydantic
from discord import SyncWebhook
from loguru import logger
from dotenv import load_dotenv
import os

from newsfeed import log_utils
from newsfeed.datatypes import BlogSummary


def load_summaries(blog_name: str) -> list[BlogSummary]:
    logger.debug(f"Processing {blog_name}")

    summaries = []
    save_dir = Path("data/data_warehouse", blog_name, "summaries")
    for summary_file in save_dir.glob("**/*.json"):
        with open(summary_file, "r") as f:
            json_data = f.read()
        summary = BlogSummary.model_validate_json(json_data)
        # logger.debug(f"Added summary: {summary}")
        summaries.append(summary)
    logger.debug(f"Summaries: {summaries}")
    return summaries

# TRASIG, ersatt med ovanstående
# def load_summaries(blog_name: str) -> list[BlogSummary]:
#     logger.debug(f"Processing {blog_name}")

#     summaries = []
#     save_dir = Path("data/datasets", blog_name, "summaries")
#     for summary_file in save_dir.glob("**/*.json"):
#         summary = pydantic.parse_file_as(BlogSummary, summary_file)
#         # logger.debug(summary)
#         summaries.append(summary)

#     return summaries

def send_to_discord(summary: BlogSummary) -> None:
    load_dotenv()
    #logger.debug(f"Sending summary to Discord: {summary.title} _step1_")
    discord_webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    webhook = SyncWebhook.from_url(discord_webhook_url)
    if not webhook:
        logger.error("Could not load webhook URL")
        return

    group_name = "isak-TEST"
    message = f"**Group name: {group_name}**\n**{summary.title}**\n```{summary.text}```"
    
    #logger.debug(f"Sending summary to Discord: {summary.title} _step2_")
    
    try:
        logger.info(f"Sent message title to Discord: {summary.title}")
        webhook.send(message)
        #logger.debug(f"Sent summary to Discord: {summary.title} _step3_")
    except Exception as e:
        logger.error(f"Failed to send message to Discord: {e}")


def main(blog_name: str) -> None:
    logger.debug(f"Processing {blog_name}")
    summaries = load_summaries(blog_name)

    # time.sleep(5) lägga en wait här då openai tar sin tid om det är många som ska göras
    
    for summary in summaries:
        send_to_discord(summary)
        #logger.debug(f"Sent summary to Discord: {summary.title} _step4_")


def parse_args() -> jsonargparse.Namespace:
    parser = jsonargparse.ArgumentParser()
    parser.add_function_arguments(main)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    log_utils.configure_logger(log_level="DEBUG")
    main(**args)
