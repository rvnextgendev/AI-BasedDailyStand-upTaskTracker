from fastapi import APIRouter, Depends, HTTPException
from ..auth import get_current_user
from ..schemas import ToolRequest, ToolResponse, UserContext
from ..rbac import is_allowed
from ..tools import TOOL_HANDLERS
from .dependencies import (
    get_task_repository,
    get_standup_repository,
    get_analytics_service,
    get_notification_service,
    get_standup_summary_service,
)

router = APIRouter(prefix="/tools", tags=["tools"])


@router.post("/{tool_name}", response_model=ToolResponse)
def call_tool(tool_name: str, req: ToolRequest, user: UserContext = Depends(get_current_user)):
    tool_info = TOOL_HANDLERS.get(tool_name)
    if not tool_info:
        raise HTTPException(status_code=404, detail=f"Unknown tool: {tool_name}")

    if not is_allowed(tool_name, user.role):
        raise HTTPException(status_code=403, detail=f"Role {user.role} not allowed for {tool_name}")

    fn = tool_info["fn"]
    deps = tool_info.get("deps", [])

    kwargs = {"args": req.args, "user": user}
    for dep in deps:
        if dep == "task_repo":
            kwargs["task_repo"] = get_task_repository()
        elif dep == "standup_repo":
            kwargs["standup_repo"] = get_standup_repository()
        elif dep == "analytics_service":
            kwargs["analytics"] = get_analytics_service()
        elif dep == "notification_service":
            kwargs["svc"] = get_notification_service()
        elif dep == "standup_summary_service":
            kwargs["summary_service"] = get_standup_summary_service()

    try:
        result = fn(**kwargs)
        return ToolResponse(success=True, data=result)
    except HTTPException:
        raise
    except Exception as ex:  # pragma: no cover - thin handler
        return ToolResponse(success=False, error=str(ex))
