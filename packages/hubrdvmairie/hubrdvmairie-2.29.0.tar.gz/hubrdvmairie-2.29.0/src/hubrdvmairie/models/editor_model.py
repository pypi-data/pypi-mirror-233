from datetime import datetime

from pydantic import BaseModel


class Editor(BaseModel):
    slug: str
    name: str
    api_url: str
    status: bool
    api_down_datetime: datetime
    api_up_datetime: datetime
    _test_mode: bool
