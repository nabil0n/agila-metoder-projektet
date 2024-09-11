from discord import SyncWebhook
from loguru import logger
from dotenv import load_dotenv
import os

from newsfeed import log_utils
from newsfeed.datatypes import BlogSummary

from S3_utils import get_s3_client

s3_client = get_s3_client()

S3_BUCKET = "my-local-bucket"
LOCALSTACK_ENDPOINT = "http://localhost:4566"
WAREHOUSE_PREFIX = "data_warehouse/"

def load_summaries(blog_name: str) -> list[BlogSummary]:
    s3_key = f"{WAREHOUSE_PREFIX}{blog_name}/summaries"
    
    logger.debug(f"Downloading summaries for {blog_name} from Localstack S3 at {s3_key}")
    
    summaries = []
    try:
        for summary in s3_client.list_objects(Bucket=S3_BUCKET, Prefix=s3_key)["Contents"]:
            logger.debug(f"Downloading summary {summary['Key']}")
            summary_data = s3_client.get_object(Bucket=S3_BUCKET, Key=summary["Key"])["Body"]
            summary_text = summary_data.read().decode("utf-8")
            summary = BlogSummary.model_validate_json(summary_text)
            summaries.append(summary)
    except Exception as e:
        logger.error(f"Failed to download summaries for {blog_name}: {str(e)}")
        raise
    
    return summaries


def send_to_discord(summary: BlogSummary) -> None:
    load_dotenv()
    #logger.debug(f"Sending summary to Discord: {summary.title} _step1_")
    discord_webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    webhook = SyncWebhook.from_url(discord_webhook_url)
    if not webhook:
        logger.error("Could not load webhook URL")
        return

    group_name = "Grupp2"
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

    log_utils.configure_logger(log_level="DEBUG")