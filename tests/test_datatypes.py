import pytest
import pydantic
from datetime import date, datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))

from newsfeed.datatypes import BlogInfo, BlogSummary

def test_blog_info_creation():
    blog_info = BlogInfo(
        unique_id="123",
        title="Test Blog",
        description="A blog for testing.",
        link="http://example.com",
        blog_text="This is a test blog post.",
        published=date(2024, 8, 20),
        timestamp=datetime(2024, 8, 20, 12, 0, 0)
    )
    assert blog_info.unique_id == "123"
    assert blog_info.title == "Test Blog"
    assert blog_info.description == "A blog for testing."
    assert blog_info.link == "http://example.com"
    assert blog_info.blog_text == "This is a test blog post."
    assert blog_info.published == date(2024, 8, 20)
    assert blog_info.timestamp == datetime(2024, 8, 20, 12, 0, 0)

def test_blog_info_filename():
    blog_info = BlogInfo(
        unique_id="123",
        title="Test Blog",
        description="A blog for testing.",
        link="http://example.com",
        blog_text="This is a test blog post.",
        published=date(2024, 8, 20),
        timestamp=datetime(2024, 8, 20, 12, 0, 0)
    )
    assert blog_info.filename == "Test_Blog.json"

def test_blog_summary_creation():
    blog_summary = BlogSummary(
        unique_id="123",
        title="Test Blog Summary",
        text="This is a summary of the test blog."
    )
    assert blog_summary.unique_id == "123"
    assert blog_summary.title == "Test Blog Summary"
    assert blog_summary.text == "This is a summary of the test blog."

def test_blog_summary_filename():
    blog_summary = BlogSummary(
        unique_id="123",
        title="Test Blog Summary",
        text="This is a summary of the test blog."
    )
    assert blog_summary.filename == "Test_Blog_Summary.json"

def test_invalid_blog_info_missing_field():
    with pytest.raises(pydantic.ValidationError):
        BlogInfo(
            unique_id="123",
            title="Test Blog",
            description="A blog for testing.",
            link="http://example.com",
            blog_text="This is a test blog post.",
            # published is missing
            timestamp=datetime(2024, 8, 20, 12, 0, 0)
        )

def test_invalid_blog_summary_missing_field():
    with pytest.raises(pydantic.ValidationError):
        BlogSummary(
            unique_id="123",
            # title is missing
            text="This is a summary of the test blog."
        )
