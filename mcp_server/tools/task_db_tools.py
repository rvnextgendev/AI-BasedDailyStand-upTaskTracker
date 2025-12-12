from typing import Any, Dict
from ..core.models import Task
from ..core.repositories import ITaskRepository
from ..schemas import TaskCreateInput, TaskListMyInput, UserContext


def create_task(args: Dict[str, Any], user: UserContext, task_repo: ITaskRepository) -> Dict[str, Any]:
    data = TaskCreateInput(**args)
    task = Task(
        id=None,
        user_id=user.user_id,
        description=data.description,
        status="PENDING",
        delay_risk=data.delay_risk or "UNKNOWN",
    )
    created = task_repo.add(task)
    return {
        "task_id": created.id,
        "description": created.description,
        "status": created.status,
        "delay_risk": created.delay_risk,
        "created_at": created.created_at.isoformat() if created.created_at else None,
    }


def list_my_tasks(args: Dict[str, Any], user: UserContext, task_repo: ITaskRepository) -> Dict[str, Any]:
    data = TaskListMyInput(**args)
    target_user_id = data.user_id or user.user_id
    tasks = task_repo.get_by_user(target_user_id)
    return {
        "user_id": target_user_id,
        "tasks": [
            {
                "id": t.id,
                "description": t.description,
                "status": t.status,
                "delay_risk": t.delay_risk,
                "created_at": t.created_at.isoformat() if t.created_at else None,
            }
            for t in tasks
        ],
    }


def list_team_tasks(args: Dict[str, Any], user: UserContext, task_repo: ITaskRepository) -> Dict[str, Any]:
    team_id = args.get("team_id")
    tasks = task_repo.get_team_tasks(team_id=team_id)
    return {
        "tasks": [
            {
                "id": t.id,
                "user_id": t.user_id,
                "description": t.description,
                "status": t.status,
                "delay_risk": t.delay_risk,
                "created_at": t.created_at.isoformat() if t.created_at else None,
            }
            for t in tasks
        ]
    }
