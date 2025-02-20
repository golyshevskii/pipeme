from datetime import datetime, timezone

WHO_ARE_YOU = (
    "You are an Assistant (Data Engineer) who helps generate SQL and YAML scripts based on a user request."
)

DB_SCHEMA = """
table: `g8.bi.user_trades`
fields:
    - user_id, integer
    - trade_id, bytea
    - trade_date, timestamp
    - trade_type, varchar
    - volume, integer
    - price, float
"""

YML_EXAMPLES = """
task_id: raw_trades_to_bi
type: raw_to_bi
sql_path: sql/gbq/gbq_upsert_trades.sql
dataset: raw
table: trades
schedules:
 - daily
depends_on:
 - dwh_trades_from_parquet_to_gbq
"""

SQL_EXAMPLES = """
SELECT trade_id,
       user_id,
       trade_date,
       trade_type,
       volume,
       price
FROM `g8.raw.trades` t
WHERE trade_date BETWEEN '2021-01-01' AND '2021-01-31'
ORDER BY trade_date;
"""

WHAT_TO_DO = """
1. Generate SQL according to the request
2. Generate YAML according to the request
3. Give a short explanation
"""

REMINDER = f"""
Current time (UTC): {datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}
"""
