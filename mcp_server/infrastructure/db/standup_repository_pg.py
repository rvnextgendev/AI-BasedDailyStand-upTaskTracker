from typing import List
from ...core.models import Standup
from ...core.repositories import IStandupRepository
from .connection import get_connection


class PgStandupRepository(IStandupRepository):
    def add(self, standup: Standup) -> Standup:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO standups (user_id, yesterday, today, blockers)
                VALUES (%s, %s, %s, %s)
                RETURNING id, created_at;
                """,
                (standup.user_id, standup.yesterday, standup.today, standup.blockers),
            )
            row = cur.fetchone()
            conn.commit()

        standup.id = row[0]
        standup.created_at = row[1]
        return standup

    def get_for_day(self, date_str: str) -> List[Standup]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, user_id, yesterday, today, blockers, created_at
                FROM standups
                WHERE DATE(created_at) = %s
                ORDER BY created_at;
                """,
                (date_str,),
            )
            rows = cur.fetchall()

        return [
            Standup(
                id=r[0],
                user_id=r[1],
                yesterday=r[2],
                today=r[3],
                blockers=r[4],
                created_at=r[5],
            )
            for r in rows
        ]
