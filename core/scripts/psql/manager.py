from typing import Any

import pandas as pd
from config import PSQL_CONN_STR
from core.scripts.psql.client import PSQLClient
from core.scripts.psql.maps import TABLE_MAP

PSQL = PSQLClient(PSQL_CONN_STR)


def select_tg_bot_user_access(user_id: int) -> pd.DataFrame:
    """Select user data from tg_bot_user_access table."""
    return PSQL.execute(
        f"""
        SELECT id, has_access
          FROM {TABLE_MAP["tg_bot_user_access"]["schema"]}.{TABLE_MAP["tg_bot_user_access"]["table"]}
         WHERE id = {user_id};
        """,
        select=True,
    )


def insert_tg_bot_user_access(user_data: dict[str, Any] | list[dict[str, Any]]) -> None:
    """Insert user data into tg_bot_user_access table."""
    PSQL.upsert(
        schema=TABLE_MAP["tg_bot_user_access"]["schema"],
        table=TABLE_MAP["tg_bot_user_access"]["table"],
        data=[user_data] if isinstance(user_data, dict) else user_data,
        on_conflict_do_update=True,
        constraint=TABLE_MAP["tg_bot_user_access"]["constraint"],
    )
