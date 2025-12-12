from typing import Dict, List

# tool_name -> allowed roles
TOOL_PERMISSIONS: Dict[str, List[str]] = {
    "task-db.create_task": ["Developer", "ScrumMaster", "Admin"],
    "task-db.list_my_tasks": ["Developer", "ScrumMaster", "Admin"],
    "task-db.list_team_tasks": ["ScrumMaster", "Admin"],
    "standup.save": ["Developer", "ScrumMaster", "Admin"],
    "standup.get_for_day": ["ScrumMaster", "Admin"],
    "standup.summarise_day": ["ScrumMaster", "Admin"],
    "analytics.team_heatmap": ["ScrumMaster", "Admin"],
    "notification.send": ["ScrumMaster", "Admin"],
    "admin.manage_users": ["Admin"],
}


def is_allowed(tool_name: str, role: str) -> bool:
    allowed = TOOL_PERMISSIONS.get(tool_name, [])
    return role in allowed
