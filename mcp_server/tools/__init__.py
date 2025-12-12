from typing import Any, Callable, Dict
from ..schemas import UserContext
from . import task_db_tools, standup_tools, analytics_tools, notification_tools

ToolHandler = Callable[..., Dict[str, Any]]

TOOL_HANDLERS: Dict[str, Dict[str, Any]] = {
    "task-db.create_task": {"fn": task_db_tools.create_task, "deps": ["task_repo"]},
    "task-db.list_my_tasks": {"fn": task_db_tools.list_my_tasks, "deps": ["task_repo"]},
    "task-db.list_team_tasks": {"fn": task_db_tools.list_team_tasks, "deps": ["task_repo"]},
    "standup.save": {"fn": standup_tools.save_standup, "deps": ["standup_repo"]},
    "standup.get_for_day": {"fn": standup_tools.get_for_day, "deps": ["standup_repo"]},
    "standup.summarise_day": {
        "fn": standup_tools.summarise_day,
        "deps": ["standup_repo", "standup_summary_service"],
    },
    "analytics.team_heatmap": {"fn": analytics_tools.team_heatmap, "deps": ["analytics_service"]},
    "notification.send": {"fn": notification_tools.send_notification, "deps": ["notification_service"]},
}
