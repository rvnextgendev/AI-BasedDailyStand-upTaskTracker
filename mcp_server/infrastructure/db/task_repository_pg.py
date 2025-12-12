from typing import List, Optional
from ...core.models import Task
from ...core.repositories import ITaskRepository
from .connection import get_connection


class PgTaskRepository(ITaskRepository):
    def add(self, task: Task) -> Task:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO tasks (user_id, description, status, delay_risk)
                VALUES (%s, %s, %s, %s)
                RETURNING id, created_at;
                """,
                (task.user_id, task.description, task.status, task.delay_risk),
            )
            row = cur.fetchone()
            conn.commit()

        task.id = row[0]
        task.created_at = row[1]
        return task

    def get_by_user(self, user_id: str) -> List[Task]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, user_id, description, status, delay_risk, created_at
                FROM tasks
                WHERE user_id = %s
                ORDER BY created_at DESC;
                """,
                (user_id,),
            )
            rows = cur.fetchall()

        return [
            Task(
                id=r[0],
                user_id=r[1],
                description=r[2],
                status=r[3],
                delay_risk=r[4],
                created_at=r[5],
            )
            for r in rows
        ]

    def get_team_tasks(self, team_id: Optional[str] = None, limit: int = 200) -> List[Task]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, user_id, description, status, delay_risk, created_at
                FROM tasks
                ORDER BY created_at DESC
                LIMIT %s;
                """,
                (limit,),
            )
            rows = cur.fetchall()

        return [
            Task(
                id=r[0],
                user_id=r[1],
                description=r[2],
                status=r[3],
                delay_risk=r[4],
                created_at=r[5],
            )
            for r in rows
        ]
