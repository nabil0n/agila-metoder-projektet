import pytest
from pathlib import Path
import requests
from unittest.mock import patch, mock_open
from newsfeed import log_utils
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))

from newsfeed.download_blogs_from_rss import get_metadata_info, save_metadata_info, main, parse_args

# Mock data
MOCK_BLOG_NAME = "mit"
MOCK_XML_TEXT = "<xml>Mock XML Content</xml>"
LINK_TO_XML_FILE = {
    "mit": "https://news.mit.edu/rss/topic/artificial-intelligence2",
}

def test_get_metadata_info_success():
    with patch('requests.get') as mock_get:
        mock_get.return_value.text = MOCK_XML_TEXT
        xml_text = get_metadata_info(MOCK_BLOG_NAME)
        assert xml_text == MOCK_XML_TEXT
        mock_get.assert_called_once_with(LINK_TO_XML_FILE[MOCK_BLOG_NAME])

def test_get_metadata_info_invalid_blog():
    with pytest.raises(AssertionError):
        get_metadata_info("invalid_blog_name")

def test_save_metadata_info():
    with patch('builtins.open', mock_open()) as mock_file:
        with patch.object(Path, 'mkdir') as mock_mkdir:
            save_metadata_info(MOCK_XML_TEXT, MOCK_BLOG_NAME)
            mock_mkdir.assert_called_once_with(exist_ok=True, parents=True)
            mock_file().write.assert_called_once_with(MOCK_XML_TEXT)

def test_main():
    with patch('requests.get') as mock_get:
        mock_get.return_value.text = MOCK_XML_TEXT
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(Path, 'mkdir') as mock_mkdir:
                with patch('loguru.logger.info') as mock_logger:
                    main(MOCK_BLOG_NAME)
                    mock_get.assert_called_once_with(LINK_TO_XML_FILE[MOCK_BLOG_NAME])
                    mock_mkdir.assert_called_once_with(exist_ok=True, parents=True)
                    mock_file().write.assert_called_once_with(MOCK_XML_TEXT)
                    mock_logger.assert_any_call(f"Processing {MOCK_BLOG_NAME}")
                    mock_logger.assert_any_call(f"Done processing {MOCK_BLOG_NAME}")

def test_parse_args():
    with patch('jsonargparse.ArgumentParser.parse_args') as mock_parse_args:
        mock_parse_args.return_value = {'blog_name': MOCK_BLOG_NAME}
        args = parse_args()
        assert args == {'blog_name': MOCK_BLOG_NAME}
        mock_parse_args.assert_called_once()
