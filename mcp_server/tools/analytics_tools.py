from typing import Any, Dict
from ..core.services import AnalyticsService
from ..schemas import TeamRiskHeatmapInput, UserContext


def team_heatmap(args: Dict[str, Any], user: UserContext, analytics: AnalyticsService) -> Dict[str, Any]:
    data = TeamRiskHeatmapInput(**args)
    return analytics.team_heatmap(team_id=data.team_id, from_date=data.from_date, to_date=data.to_date)
