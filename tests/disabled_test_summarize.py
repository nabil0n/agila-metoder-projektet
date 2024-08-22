import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
from newsfeed.datatypes import BlogInfo, BlogSummary

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))

from newsfeed.summarize import (
    load_articles,
    save_summaries,
    create_summaries,
    main,
    parse_args,
)

# Mock data
MOCK_BLOG_NAME = "mit"
MOCK_ARTICLE_JSON = """
{
    "unique_id": "123",
    "title": "Test Article",
    "description": "Test Description",
    "link": "http://example.com/test-article",
    "blog_text": "This is a test blog post.",
    "published": "2024-08-20",
    "timestamp": "2024-08-20T12:00:00"
}
"""
MOCK_ARTICLE_OBJECT = BlogInfo(
    unique_id="123",
    title="Test Article",
    description="Test Description",
    link="http://example.com/test-article",
    blog_text="This is a test blog post.",
    published="2024-08-20",
    timestamp="2024-08-20T12:00:00",
)

MOCK_SUMMARY_OBJECT = BlogSummary(
    unique_id="123",
    title="Test Article",
    text="This is a summarized version of the test blog post."
)

def test_load_articles():
    with patch('builtins.open', mock_open(read_data=MOCK_ARTICLE_JSON)):
        with patch.object(Path, 'glob', return_value=[Path("mock_article.json")]):
            articles = load_articles(MOCK_BLOG_NAME)
            assert len(articles) == 1
            assert articles[0] == MOCK_ARTICLE_OBJECT

def test_save_summaries():
    summaries = [MOCK_SUMMARY_OBJECT]

    with patch('builtins.open', mock_open()) as mock_file:
        with patch.object(Path, 'mkdir') as mock_mkdir:
            save_summaries(summaries, MOCK_BLOG_NAME)
            mock_mkdir.assert_called_once_with(exist_ok=True, parents=True)
            mock_file().write.assert_called_once_with(summaries[0].json(indent=2))

@patch('summarize.ChatOpenAI')
@patch('summarize.load_summarize_chain')
def test_create_summaries(mock_load_summarize_chain, mock_ChatOpenAI):
    mock_chain = mock_load_summarize_chain.return_value
    mock_chain.run.return_value = "This is a summarized version of the test blog post."
    
    summaries = create_summaries([MOCK_ARTICLE_OBJECT], summary_type="default")
    
    assert len(summaries) == 1
    assert summaries[0] == MOCK_SUMMARY_OBJECT
    mock_ChatOpenAI.assert_called_once_with(temperature=0, model_name="gpt-3.5-turbo")
    mock_load_summarize_chain.assert_called_once()

def test_main():
    with patch('summarize.load_articles', return_value=[MOCK_ARTICLE_OBJECT]) as mock_load_articles:
        with patch('summarize.create_summaries', return_value=[MOCK_SUMMARY_OBJECT]) as mock_create_summaries:
            with patch('summarize.save_summaries') as mock_save_summaries:
                with patch('loguru.logger.debug') as mock_logger:
                    main(MOCK_BLOG_NAME)
                    
                    mock_logger.assert_any_call(f"Processing {MOCK_BLOG_NAME}")
                    mock_load_articles.assert_called_once_with(MOCK_BLOG_NAME)
                    mock_create_summaries.assert_called_once_with([MOCK_ARTICLE_OBJECT], "default")
                    mock_save_summaries.assert_called_once_with([MOCK_SUMMARY_OBJECT], MOCK_BLOG_NAME)

def test_parse_args():
    with patch('jsonargparse.ArgumentParser.parse_args') as mock_parse_args:
        mock_parse_args.return_value = {'blog_name': MOCK_BLOG_NAME, 'summary_type': 'default'}
        args = parse_args()
        assert args == {'blog_name': MOCK_BLOG_NAME, 'summary_type': 'default'}
        mock_parse_args.assert_called_once()
