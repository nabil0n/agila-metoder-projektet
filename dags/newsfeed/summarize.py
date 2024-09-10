import boto3
from pathlib import Path

from dotenv import load_dotenv
import jsonargparse
import pydantic
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from loguru import logger

from newsfeed import log_utils
from newsfeed.datatypes import BlogInfo, BlogSummary

from S3_compabillity import get_s3_client

S3_BUCKET = "my-local-bucket"
LOCALSTACK_ENDPOINT = "http://localstack:4566"
WAREHOUSE_PREFIX = "data-warehouse/"

DEFAULT_PROMPT_TEMPLATE = """
Write a concise summary of the following:
{text}
"""

NON_TECHNICAL_PROMPT_TEMPLATE = """
Write a concise, easy to understand, and non techincal summary of the following:
{text}
"""

PROMPT_TEMPLATES = {
    "default": DEFAULT_PROMPT_TEMPLATE,
    "non_technical": NON_TECHNICAL_PROMPT_TEMPLATE,
}

# NEDAN UTKOMMENTERAT ÄR FÖR ATT KÖRA LOKALT
# def load_articles(blog_name: str) -> list[BlogInfo]:
#     articles = []
#     save_dir = Path("data/data_warehouse", blog_name, "articles")
#     for article_file in save_dir.glob("**/*.json"):
#         with open(article_file, "r") as f:
#             json_data = f.read()
#         article = BlogInfo.model_validate_json(json_data)
#         articles.append(article)

#     return articles

# TRASIG, ersatt med ovanstående
# def load_articles(blog_name: str) -> list[BlogInfo]:
#     articles = []
#     save_dir = Path("data/data_warehouse", blog_name, "articles")
#     for article_file in save_dir.glob("**/*.json"):
#         article = pydantic.parse_file_as(BlogInfo, article_file)
#         articles.append(article)

#     return articles

def load_articles(blog_name: str) -> list[BlogInfo]:
    s3_client = get_s3_client()
    s3_prefix = f"{WAREHOUSE_PREFIX}{blog_name}/articles/"

    response = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix=s3_prefix)
    articles = []

    for obj in response.get('Contents', []):
        article_key = obj['Key']
        try:
            article_obj = s3_client.get_object(Bucket=S3_BUCKET, Key=article_key)
            json_data = article_obj['Body'].read().decode('utf-8')
            article = BlogInfo.model_validate_json(json_data)
            articles.append(article)
        except Exception as e:
            logger.error(f"Error loadin article {article_key} from S3: {e}")

    return articles

# NEDAN UTKOMMENTERAT ÄR FÖR ATT KÖRA LOKALT
# def save_summaries(summaries: list[BlogSummary], blog_name: str) -> None:
#     save_dir = Path("data/data_warehouse", blog_name, "summaries")
#     save_dir.mkdir(exist_ok=True, parents=True)
#     for summary in summaries:
#         save_path = save_dir / summary.filename
#         with open(save_path, "w") as f:
#             f.write(summary.to_json())

def save_summaries(summaries: list[BlogSummary], blog_name: str) -> None:
    s3_client = get_s3_client()

    for summary in summaries:
        s3_key = f"{WAREHOUSE_PREFIX}{blog_name}/summaries/{summary.filename}"
        try:
            s3_client.put_object(
                Bucket = S3_BUCKET,
                Key = s3_key,
                Body = summary.to_json().encode('utf-8')
            )
            logger.info(f"Saved summary {summary.unique_id} to S3 at {s3_key}")
        except Exception as e:
            logger.error(f"Error saving summary {summary.unique_id} to S3: {e}")

def create_summaries(articles: list[BlogInfo], summary_type: str) -> list[BlogSummary]:
    load_dotenv()
    model_name = "gpt-3.5-turbo"
    llm = ChatOpenAI(temperature=0, model_name=model_name)
    text_splitter = CharacterTextSplitter()

    """
    Om denna inte är här så tar det ganska lång tid att genomföra summeringarna.
    Då den kontaktar openai för varje artikel. Så kommentera av denna sen i skarpt läge.
    """
    articles = articles[3:6] # Denna alltså.

    summaries = []
    for article in articles:
        texts = text_splitter.split_text(article.blog_text)
        docs = [Document(page_content=text) for text in texts]

        prompt_template = PROMPT_TEMPLATES[summary_type]
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
        chain = load_summarize_chain(llm, chain_type="stuff", prompt=PROMPT)

        output = chain.run(docs)
        logger.debug(f"\n{output}")

        summary = BlogSummary(text=output, title=article.title, unique_id=article.unique_id)
        summaries.append(summary)

    return summaries


def main(blog_name: str, summary_type: str = "default") -> None:
    logger.debug(f"Processing {blog_name}")
    articles = load_articles(blog_name)
    summaries = create_summaries(articles, summary_type)
    save_summaries(summaries, blog_name)


def parse_args() -> jsonargparse.Namespace:
    parser = jsonargparse.ArgumentParser()
    parser.add_function_arguments(main)
    return parser.parse_args()


if __name__ == "__main__":
    # dotenv.load_dotenv("../cfg/dev.env")
    args = parse_args()
    log_utils.configure_logger(log_level="DEBUG")
    main(**args)
