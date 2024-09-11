from loguru import logger

from newsfeed import log_utils
from S3_utils import get_s3_client

s3_client = get_s3_client()

S3_BUCKET = "my-local-bucket"
S3_PREFIX = "data_lake/"
WAREHOUSE_PREFIX = "data_warehouse/"
LOCALSTACK_ENDPOINT = "http://localhost:4566"

def delete_files() -> None:
    try:
        lake_response = s3_client.list_objects(Bucket=S3_BUCKET, Prefix=S3_PREFIX)
        wh_response = s3_client.list_objects(Bucket=S3_BUCKET, Prefix=WAREHOUSE_PREFIX)
        
        if "Contents" in lake_response:
            
            for item in lake_response["Contents"]:
                s3_client.delete_object(Bucket=S3_BUCKET, Key=item["Key"])
                logger.info(f"Deleted {item['Key']} from S3")
                
            for item in wh_response["Contents"]:
                s3_client.delete_object(Bucket=S3_BUCKET, Key=item["Key"])
                logger.info(f"Deleted {item['Key']} from S3")
        else:
            logger.info(f"No files to delete in {S3_BUCKET}")
    except Exception as e:
        logger.error(f"Failed to delete files from {S3_BUCKET}: {str(e)}")
        raise

def main() -> None:
    logger.info(f"Deleting files from {S3_BUCKET}")
    delete_files()
    logger.info(f"Done deleting files from {S3_BUCKET}")
    log_utils.configure_logger(log_level="DEBUG")