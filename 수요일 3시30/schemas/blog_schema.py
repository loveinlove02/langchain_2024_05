from pydantic.dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class BlogData:
    id: int
    title: str
    author: str
    content: str
    modified_dt: datetime
    image_loc: str | None = None
