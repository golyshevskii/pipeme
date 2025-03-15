TABLE_MAP = {
    "tg_bot_user_access": {
        "schema": "raw",
        "table": "tg_bot_user_access",
        "constraint": "tg_bot_user_access_pk",
        "sql": """
        CREATE TABLE IF NOT EXISTS raw.tg_bot_user_access (
            id bigserial NOT NULL,
            username varchar(256) NOT NULL,
            has_access boolean DEFAULT False,
            record_update_dtt timestamptz DEFAULT CURRENT_TIMESTAMP,
            record_load_dtt timestamptz DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT tg_bot_user_access_pk PRIMARY KEY (id)
        );
        """,
    },
}
