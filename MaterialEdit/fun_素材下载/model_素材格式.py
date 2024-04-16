from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MaterialModel(BaseModel):
    url: str
    img: str

    name: Optional[str] = None
    img_list: Optional[list[str]] = None

    state: bool

    create_date: Optional[datetime] = None
