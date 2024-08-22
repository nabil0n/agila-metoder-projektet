import uuid
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, mock_open
from bs4 import BeautifulSoup
from newsfeed.datatypes import BlogInfo

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))

from newsfeed.extract_articles import (
    create_uuid_from_string, 
    load_metadata, 
    extract_articles_from_xml, 
    save_articles, 
    main, 
    parse_args
)

# Mock data
MOCK_BLOG_NAME = "mit"
MOCK_XML_CONTENT = """
<rss>
  <channel>
    <item>
      <title>Test Article</title>
      <description>Test Description</description>
      <link>http://example.com/test-article</link>
      <pubDate>Mon, 20 Aug 2024 12:00:00 GMT</pubDate>
      <content:encoded><![CDATA[<p>This is a test article.</p>]]></content:encoded>
    </item>
  </channel>
</rss>
"""

def test_create_uuid_from_string():
    test_string = "Test Article"
    generated_uuid = create_uuid_from_string(test_string)
    expected_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, test_string))
    assert generated_uuid == expected_uuid

def test_load_metadata():
    with patch('builtins.open', mock_open(read_data=MOCK_XML_CONTENT)):
        with patch.object(Path, 'exists', return_value=True):
            parsed_xml = load_metadata(MOCK_BLOG_NAME)
            assert isinstance(parsed_xml, BeautifulSoup)
            assert parsed_xml.find("title").text == "Test Article"

def test_extract_articles_from_xml():
    parsed_xml = BeautifulSoup(MOCK_XML_CONTENT, "xml")
    articles = extract_articles_from_xml(parsed_xml)
    assert len(articles) == 1
    article = articles[0]
    assert isinstance(article, BlogInfo)
    assert article.title == "Test Article"
    assert article.description == "Test Description"
    assert article.link == "http://example.com/test-article"
    assert article.blog_text == "This is a test article."
    assert article.published == datetime(2024, 8, 20).date()

def test_save_articles():
    articles = [BlogInfo(
        unique_id="123",
        title="Test Article",
        description="Test Description",
        link="http://example.com/test-article",
        blog_text="This is a test article.",
        published=datetime(2024, 8, 20).date(),
        timestamp=datetime.now(),
    )]

    with patch('builtins.open', mock_open()) as mock_file:
        with patch.object(Path, 'mkdir') as mock_mkdir:
            save_articles(articles, MOCK_BLOG_NAME)
            mock_mkdir.assert_called_once_with(exist_ok=True, parents=True)
            mock_file().write.assert_called_once_with(articles[0].json(indent=2))

def test_main():
    with patch('builtins.open', mock_open(read_data=MOCK_XML_CONTENT)):
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(Path, 'mkdir') as mock_mkdir:
                with patch('loguru.logger.info') as mock_logger:
                    main(MOCK_BLOG_NAME)
                    mock_mkdir.assert_called_once_with(exist_ok=True, parents=True)
                    mock_file().write.assert_called()
                    mock_logger.assert_any_call(f"Processing {MOCK_BLOG_NAME}")
                    mock_logger.assert_any_call(f"Done processing {MOCK_BLOG_NAME}")

def test_parse_args():
    with patch('jsonargparse.ArgumentParser.parse_args') as mock_parse_args:
        mock_parse_args.return_value = {'blog_name': MOCK_BLOG_NAME}
        args = parse_args()
        assert args == {'blog_name': MOCK_BLOG_NAME}
        mock_parse_args.assert_called_once()
