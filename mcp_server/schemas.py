from typing import Any, Dict, Optional
from pydantic import BaseModel


class UserContext(BaseModel):
    user_id: str
    name: Optional[str] = None
    role: str


class ToolRequest(BaseModel):
    args: Dict[str, Any] = {}


class ToolResponse(BaseModel):
    success: bool = True
    data: Any = None
    error: Optional[str] = None


class TaskCreateInput(BaseModel):
    description: str
    delay_risk: Optional[str] = None


class TaskListMyInput(BaseModel):
    user_id: Optional[str] = None


class StandupSaveInput(BaseModel):
    yesterday: str
    today: str
    blockers: Optional[str] = None


class TeamRiskHeatmapInput(BaseModel):
    team_id: str
    from_date: str
    to_date: str


class SendNotificationInput(BaseModel):
    to: str
    channel: str  # email or whatsapp
    subject: Optional[str] = None
    message: str
