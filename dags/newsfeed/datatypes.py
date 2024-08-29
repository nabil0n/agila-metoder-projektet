from datetime import date, datetime
import json
import pydantic


class BlogInfo(pydantic.BaseModel):
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
    unique_id: str  # This should be the same as for BlogInfo so that they can be linked
    title: str
    text: str

    @property
    def filename(self) -> str:
        return f'{self.title.replace(" ", "_")}.json'

    def to_json(self) -> str:
        return json.dumps(self.dict(), default=str, indent=4)