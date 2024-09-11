from datetime import date, datetime
import json
import pydantic


class BlogInfo(pydantic.BaseModel):
    """
    Represents information about a blog post.
    Attributes:
        unique_id (str): The unique identifier of the blog post.
        title (str): The title of the blog post.
        description (str): The description of the blog post.
        link (str): The link to the blog post.
        blog_text (str): The content of the blog post.
        published (date): The date when the blog post was published.
        timestamp (datetime): The timestamp of the blog post.
    Methods:
        filename() -> str:
            Returns the filename for the blog post in JSON format.
        to_json() -> str:
            Returns the JSON representation of the blog post.
    """
    unique_id: str
    title: str
    description: str
    link: str
    blog_text: str
    published: date
    timestamp: datetime

    @property
    def filename(self) -> str:
        return f'{self.title.replace(" ", "_")}.json'

    def to_json(self) -> str:
        return json.dumps(self.dict(), default=str, indent=4)

class BlogSummary(pydantic.BaseModel):
    """
    Represents a summary of a blog post.
    Attributes:
        unique_id (str): The unique identifier of the blog post.
        title (str): The title of the blog post.
        text (str): The text content of the blog post.
    Methods:
        filename() -> str: Returns the filename for the blog post in JSON format.
        to_json() -> str: Converts the blog summary object to a JSON string.
    """
    unique_id: str  # This should be the same as for BlogInfo so that they can be linked
    title: str
    text: str

    @property
    def filename(self) -> str:
        return f'{self.title.replace(" ", "_")}.json'

    def to_json(self) -> str:
        return json.dumps(self.dict(), default=str, indent=4)