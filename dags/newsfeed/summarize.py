from dotenv import load_dotenv
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from loguru import logger
from newsfeed.datatypes import BlogInfo, BlogSummary
from S3_utils import get_s3_client

from newsfeed import log_utils

s3_client = get_s3_client()

S3_BUCKET = "my-local-bucket"
LOCALSTACK_ENDPOINT = "http://localhost:4566"
WAREHOUSE_PREFIX = "data_warehouse/"

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


def load_articles(blog_name: str) -> list[BlogInfo]:
    """
    Load articles for a given blog name.
    Args:
        blog_name (str): The name of the blog.
    Returns:
        list[BlogInfo]: A list of BlogInfo objects representing the articles.
    Raises:
        Exception: If there is an error downloading the articles.
    """

    s3_key = f"{WAREHOUSE_PREFIX}{blog_name}/articles"
    articles = []
    logger.debug(f"Downloading articles for {blog_name} from Localstack S3 at {s3_key}")

    try:
        for article in s3_client.list_objects(Bucket=S3_BUCKET, Prefix=s3_key)["Contents"]:
            logger.debug(f"Downloading article {article['Key']}")
            article_key = article["Key"]
            article_obj = s3_client.get_object(Bucket=S3_BUCKET, Key=article_key)
            article_text = article_obj["Body"].read().decode("utf-8")
            article = BlogInfo.model_validate_json(article_text)
            articles.append(article)
    except Exception as e:
        logger.error(f"Failed to download articles for {blog_name}: {str(e)}")
        raise

    return articles


def save_summaries(summaries: list[BlogSummary], blog_name: str) -> None:
    """
    Save the given list of blog summaries to an S3 bucket.
    Parameters:
    - summaries (list[BlogSummary]): A list of BlogSummary objects representing the summaries to be saved.
    - blog_name (str): The name of the blog.
    Returns:
    None
    """

    for summary in summaries:
        s3_key = f"{WAREHOUSE_PREFIX}{blog_name}/summaries/{summary.filename}"
        try:
            s3_client.put_object(
                Bucket=S3_BUCKET, Key=s3_key, Body=summary.to_json().encode("utf-8")
            )
            logger.info(f"Saved summary {summary.filename} to S3 at {s3_key}")
        except Exception as e:
            logger.error(f"Failed to save summary {summary.filename} to S3 at {s3_key}: {str(e)}")
            continue


def create_summaries(articles: list[BlogInfo], summary_type: str) -> list[BlogSummary]:
    """
    Creates summaries for a list of articles.
    Args:
        articles (list[BlogInfo]): A list of BlogInfo objects representing the articles to be summarized.
        summary_type (str): The type of summary to be generated.
    Returns:
        list[BlogSummary]: A list of BlogSummary objects representing the generated summaries.
    """
    load_dotenv()
    model_name = "gpt-3.5-turbo"
    llm = ChatOpenAI(temperature=0, model_name=model_name)
    text_splitter = CharacterTextSplitter()

    """
    Om denna inte är här så tar det ganska lång tid att genomföra summeringarna.
    Då den kontaktar openai för varje artikel. Så kommentera av denna sen i skarpt läge.
    """
    articles = articles[:1]  # Denna alltså.

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
    log_utils.configure_logger(log_level="DEBUG")
