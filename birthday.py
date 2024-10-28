from dataclasses import dataclass
from datetime import datetime


@dataclass
class Birthday:
    item_id: int
    user_id: int
    name: str
    date: datetime
