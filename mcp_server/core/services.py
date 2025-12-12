from dataclasses import dataclass
from typing import Any, Dict, List
from .models import Task, Standup
from .repositories import ITaskRepository


class INotificationClient:
    def send(self, to: str, channel: str, subject: str | None, message: str) -> None:
        raise NotImplementedError


class IMLClient:
    def predict_delay(self, task_description: str) -> Dict[str, Any]:
        raise NotImplementedError


class ILLMClient:
    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError


@dataclass
class AnalyticsService:
    task_repo: ITaskRepository
    ml_client: IMLClient

    def team_heatmap(self, team_id: str, from_date: str, to_date: str) -> Dict[str, Any]:
        tasks = self.task_repo.get_team_tasks(team_id=team_id)
        data: List[Dict[str, Any]] = []
        for t in tasks:
            data.append(
                {
                    "user_id": t.user_id,
                    "description": t.description,
                    "delay_risk": t.delay_risk,
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                }
            )

        return {
            "team_id": team_id,
            "from_date": from_date,
            "to_date": to_date,
            "data": data,
        }


@dataclass
class NotificationService:
    client: INotificationClient

    def send(self, to: str, channel: str, subject: str | None, message: str) -> Dict[str, Any]:
        self.client.send(to=to, channel=channel, subject=subject, message=message)
        return {"status": "sent", "channel": channel, "to": to}


@dataclass
class StandupSummaryService:
    llm: ILLMClient

    def summarise_day(self, raw_standups: str) -> str:
        system_prompt = (
            "You are a Scrum Master assistant. Summarize team stand-ups into concise bullets: "
            "completed work, planned work, and blockers."
        )
        return self.llm.generate_text(system_prompt, raw_standups)
