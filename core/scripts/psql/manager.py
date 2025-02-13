from typing import Any, Dict, List, Union

import pandas as pd
from config import PSQL_CONN_STR
from core.scripts.psql.client import PSQLClient
from core.scripts.psql.table_map import RAW

DWH = PSQLClient(PSQL_CONN_STR)


def select_user(user_id: int) -> pd.DataFrame:
    return DWH.execute(
        f"""
        SELECT id, has_access
          FROM {RAW['users']['schema']}.{RAW['users']['table']}
         WHERE id = {user_id};
        """,
        select=True,
    )


def insert_user(user_data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> None:
    DWH.insert(
        schema=RAW["users"]["schema"],
        table=RAW["users"]["table"],
        data=[user_data] if isinstance(user_data, dict) else user_data,
        on_conflict_do_update=True,
        constraint=RAW["users"]["constraint"],
    )
