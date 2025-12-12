from functools import lru_cache
from ..core.repositories import ITaskRepository, IStandupRepository
from ..core.services import (
    AnalyticsService,
    NotificationService,
    IMLClient,
    ILLMClient,
    StandupSummaryService,
)
from ..infrastructure.db.task_repository_pg import PgTaskRepository
from ..infrastructure.db.standup_repository_pg import PgStandupRepository
from ..infrastructure.providers.ml_client import (
    LocalMLClient,
    AzureMLClient,
    BedrockMLClient,
    GoogleVertexMLClient,
)
from ..infrastructure.providers.notification_client import HttpNotificationClient
from ..infrastructure.providers.llm_client import (
    LocalOllamaLLMClient,
    AzureOpenAILLMClient,
    BedrockLLMClient,
    GoogleVertexLLMClient,
)
from ..config import get_settings

settings = get_settings()


@lru_cache
def get_task_repository() -> ITaskRepository:
    return PgTaskRepository()


@lru_cache
def get_standup_repository() -> IStandupRepository:
    return PgStandupRepository()


@lru_cache
def get_ml_client() -> IMLClient:
    provider = settings.ML_PROVIDER.upper()
    if provider == "LOCAL":
        return LocalMLClient()
    if provider == "AZURE":
        return AzureMLClient()
    if provider == "BEDROCK":
        return BedrockMLClient()
    if provider == "GCP":
        return GoogleVertexMLClient()
    return LocalMLClient()


@lru_cache
def get_analytics_service() -> AnalyticsService:
    return AnalyticsService(task_repo=get_task_repository(), ml_client=get_ml_client())


@lru_cache
def get_notification_service() -> NotificationService:
    return NotificationService(client=HttpNotificationClient())


@lru_cache
def get_llm_client() -> ILLMClient:
    provider = settings.LLM_PROVIDER.upper()
    if provider == "LOCAL":
        return LocalOllamaLLMClient()
    if provider == "AZURE":
        return AzureOpenAILLMClient()
    if provider == "BEDROCK":
        return BedrockLLMClient()
    if provider == "GCP":
        return GoogleVertexLLMClient()
    return LocalOllamaLLMClient()


@lru_cache
def get_standup_summary_service() -> StandupSummaryService:
    return StandupSummaryService(llm=get_llm_client())
