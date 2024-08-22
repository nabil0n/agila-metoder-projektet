from pathlib import Path

import dotenv
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
    articles = []
    save_dir = Path("data/data_warehouse", blog_name, "articles")
    for article_file in save_dir.glob("**/*.json"):
        article = pydantic.parse_file_as(BlogInfo, article_file)
        articles.append(article)

    return articles


def save_summaries(summaries: list[BlogSummary], blog_name: str) -> None:
    save_dir = Path("data/data_warehouse", blog_name, "summaries")
    save_dir.mkdir(exist_ok=True, parents=True)
    for summary in summaries:
        save_path = save_dir / summary.filename
        with open(save_path, "w") as f:
            f.write(summary.json(indent=2))


def create_summaries(articles: list[BlogInfo], summary_type: str) -> list[BlogSummary]:
    model_name = "gpt-3.5-turbo"
    llm = ChatOpenAI(temperature=0, model_name=model_name)
    text_splitter = CharacterTextSplitter()

    articles = articles[:1]  # TODO: Remove

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
    dotenv.load_dotenv("cfg/dev.env")
    args = parse_args()
    log_utils.configure_logger(log_level="DEBUG")
    main(**args)
