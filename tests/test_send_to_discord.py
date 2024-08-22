from pathlib import Path
from unittest.mock import patch, mock_open

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))

from newsfeed.datatypes import BlogSummary
from newsfeed.send_to_discord import load_summaries, send_to_discord, main, parse_args

# Mock data
MOCK_BLOG_NAME = "mit"
MOCK_SUMMARY_JSON = """
{
    "unique_id": "123",
    "title": "Test Summary",
    "text": "This is a summary of the test blog."
}
"""
MOCK_SUMMARY_OBJECT = BlogSummary(
    unique_id="123",
    title="Test Summary",
    text="This is a summary of the test blog."
)

def test_load_summaries():
    with patch('builtins.open', mock_open(read_data=MOCK_SUMMARY_JSON)):
        with patch.object(Path, 'glob', return_value=[Path("mock_summary.json")]):
            summaries = load_summaries(MOCK_BLOG_NAME)
            assert len(summaries) == 1
            assert summaries[0] == MOCK_SUMMARY_OBJECT

@patch('send_to_discord.SyncWebhook')
def test_send_to_discord(mock_webhook_class):
    mock_webhook = mock_webhook_class.from_url.return_value

    send_to_discord(MOCK_SUMMARY_OBJECT)

    expected_message = (
        "**Group name: <NoName>**\n"
        "**Test Summary**\n"
        "```This is a summary of the test blog.```"
    )
    mock_webhook.send.assert_called_once_with(expected_message)

def test_main():
    with patch('send_to_discord.load_summaries', return_value=[MOCK_SUMMARY_OBJECT]) as mock_load_summaries:
        with patch('send_to_discord.send_to_discord') as mock_send_to_discord:
            with patch('loguru.logger.debug') as mock_logger:
                main(MOCK_BLOG_NAME)
                
                mock_logger.assert_any_call(f"Processing {MOCK_BLOG_NAME}")
                mock_load_summaries.assert_called_once_with(MOCK_BLOG_NAME)
                mock_send_to_discord.assert_called_once_with(MOCK_SUMMARY_OBJECT)

def test_parse_args():
    with patch('jsonargparse.ArgumentParser.parse_args') as mock_parse_args:
        mock_parse_args.return_value = {'blog_name': MOCK_BLOG_NAME}
        args = parse_args()
        assert args == {'blog_name': MOCK_BLOG_NAME}
        mock_parse_args.assert_called_once()
