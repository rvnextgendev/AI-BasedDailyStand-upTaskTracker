from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Task, Standup


class ITaskRepository(ABC):
    @abstractmethod
    def add(self, task: Task) -> Task:
        raise NotImplementedError

    @abstractmethod
    def get_by_user(self, user_id: str) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    def get_team_tasks(self, team_id: Optional[str] = None, limit: int = 200) -> List[Task]:
        raise NotImplementedError


class IStandupRepository(ABC):
    @abstractmethod
    def add(self, standup: Standup) -> Standup:
        raise NotImplementedError

    @abstractmethod
    def get_for_day(self, date_str: str) -> List[Standup]:
        raise NotImplementedError
