from typing import Any, Dict, List
from ..core.models import Standup
from ..core.repositories import IStandupRepository
from ..core.services import StandupSummaryService
from ..schemas import StandupSaveInput, UserContext


def save_standup(args: Dict[str, Any], user: UserContext, standup_repo: IStandupRepository) -> Dict[str, Any]:
    data = StandupSaveInput(**args)
    standup = Standup(
        id=None,
        user_id=user.user_id,
        yesterday=data.yesterday,
        today=data.today,
        blockers=data.blockers,
    )
    created = standup_repo.add(standup)
    return {
        "standup_id": created.id,
        "created_at": created.created_at.isoformat() if created.created_at else None,
    }


def get_for_day(args: Dict[str, Any], user: UserContext, standup_repo: IStandupRepository) -> Dict[str, Any]:
    target_date = args.get("date")
    if not target_date:
        raise ValueError("date is required (YYYY-MM-DD)")

    standups: List[Standup] = standup_repo.get_for_day(target_date)
    return {
        "date": target_date,
        "standups": [
            {
                "id": s.id,
                "user_id": s.user_id,
                "yesterday": s.yesterday,
                "today": s.today,
                "blockers": s.blockers,
                "created_at": s.created_at.isoformat() if s.created_at else None,
            }
            for s in standups
        ],
    }


def summarise_day(
    args: Dict[str, Any],
    user: UserContext,
    standup_repo: IStandupRepository,
    summary_service: StandupSummaryService,
) -> Dict[str, Any]:
    date_str = args.get("date")
    if not date_str:
        raise ValueError("date is required (YYYY-MM-DD)")

    standups: List[Standup] = standup_repo.get_for_day(date_str)
    lines = []
    for s in standups:
        lines.append(f"User {s.user_id}:")
        lines.append(f"  Yesterday: {s.yesterday}")
        lines.append(f"  Today: {s.today}")
        lines.append(f"  Blockers: {s.blockers or 'None'}")
        lines.append("")

    raw_text = "\n".join(lines)
    summary = summary_service.summarise_day(raw_text)
    return {"date": date_str, "summary": summary, "raw_count": len(standups)}
