from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    id: Optional[int]
    user_id: str
    description: str
    status: str
    delay_risk: str
    created_at: Optional[datetime] = None


@dataclass
class Standup:
    id: Optional[int]
    user_id: str
    yesterday: str
    today: str
    blockers: Optional[str]
    created_at: Optional[datetime] = None
