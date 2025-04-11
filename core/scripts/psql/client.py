from logging import INFO
from typing import Any

import pandas as pd
import psycopg2
import sshtunnel
from core.scripts.tools.files import read_file
from logs.logger import get_logger
from psycopg2.extras import execute_batch
from sqlalchemy import create_engine, text

logger = get_logger(__name__, level=INFO)


class PSQLQueryBuilder:
    """Class for building PSQL queries."""

    @staticmethod
    def build_upsert_query(
        schema: str,
        table: str,
        columns: list[dict],
        update_columns: list[str] | None = None,
        do_nothing: bool = False,
        do_update: bool = False,
        constraint: str = None,
        pkeys: list[str] | None = None,
    ) -> str:
        """
        Return specific upsert query, depending on the parameters.

        Params
        ------
        schema: Schema name
        table: Table name
        columns: List of table columns
        update_columns: List of columns to update
        do_nothing: If True, the ON CONFLICT DO NOTHING method will be used
        do_update: If True, the ON CONFLICT DO UPDATE SET method will be used
        constraint: The name of the constraint for the
            ON CONFLICT ON CONSTRAINT constraint DO UPDATE SET clause
        pkeys: The primary keys of the table wich will be used in the
            ON CONFLICT (pkeys) DO UPDATE SET clause
        """
        if update_columns is None and pkeys:
            update_columns = [col for col in columns if col not in pkeys]
        else:
            update_columns = columns

        attributes = ",".join(columns)

        values = [f"%({column})s" for column in columns]
        values = ",".join(values)

        on_conflict_clause, action = "", ""
        if do_update or do_nothing:
            on_conflict_clause = "ON CONFLICT " + (f"({','.join(pkeys)})" if pkeys else f"ON CONSTRAINT {constraint}")

            action = "DO NOTHING"
            if do_update:
                duplicates = [f"{column}=%({column})s" for column in update_columns]
                duplicates = ",".join(duplicates)

                action = f"DO UPDATE SET {duplicates}"

        query = f"""
        INSERT INTO {schema}.{table} ({attributes})
        VALUES ({values})
        {on_conflict_clause}
        {action};
        """
        return query


class PSQLClient:
    """
    Class for working with PostgreSQL database.

    Params
    ------
    conn_str: PSQL connection string.
        Use it if you want to connect to PSQL directly (not through SSH)
    username: PSQL username
    password: PSQL password
    db: PSQL database
    ssh_address_or_host: SSH address or host. For example: ("11.222.33.44", 22)
    ssh_username: SSH username
    ssh_pkey: SSH private key str or path to the private key file
    remote_bind_address: Remote bind address. For example: ("11.222.3.4", 5432)

    Attributes
    ----------
    conn_str: Connection string. Used for direct connection
    conn_params: Connection parameters. Used for SSH connection
    ssh_params: SSH connection parameters
    ssh_tunnel: SSH tunnel
    engine: SQLAlchemy engine for working with queries
    CONN_STR_PATTERN: Connection string pattern. Used for SSH connection
    """

    CONN_STR_PATTERN = "postgresql://%(username)s:%(password)s@%(host)s:%(port)d/%(db)s"

    def __init__(
        self,
        conn_str: str = None,
        username: str = None,
        password: str = None,
        db: str = None,
        ssh_address_or_host: tuple = None,
        ssh_username: str = None,
        ssh_pkey: str = None,
        local_bind_address: tuple = None,
        remote_bind_address: tuple = None,
    ):
        self.conn_str = conn_str
        self.conn_params = {"username": username, "password": password, "host": None, "port": None, "db": db}

        self.ssh_params = {
            "ssh_address_or_host": ssh_address_or_host,
            "ssh_username": ssh_username,
            "ssh_pkey": ssh_pkey,
            "local_bind_address": local_bind_address,
            "remote_bind_address": remote_bind_address,
        }
        self.ssh_tunnel = None
        self.engine = None

    def execute(self, sql: str, select: bool = False, payload: dict[str, Any] | None = None) -> pd.DataFrame | None:
        """
        Execute SQL query.

        Params
        ------
        sql: SQL query or path to the SQL file
        select: If True, returns the result of the query as a DataFrame
        format: Additional parameters for the SQL query
        """
        if sql.endswith(".sql"):
            sql = read_file(sql)

        if payload:
            sql = sql.format(**payload)

        self._connect()
        with self.engine.connect() as connection:
            data = None

            if select:
                data = pd.read_sql(sql=sql, con=connection)
                logger.info("Data has been extracted. Shape: %(shape)s", {"shape": data.shape})
            else:
                result = connection.execute(text(sql))
                connection.commit()
                logger.debug("SQL has been executed. Effected rows: %(rowcount)s", {"rowcount": result.rowcount})
        self._disconnect()

        return data

    def upsert(
        self,
        schema: str,
        table: str,
        data: list[dict[str, Any]],
        on_conflict_do_nothing: bool = False,
        on_conflict_do_update: bool = False,
        update_columns: list[str] | None = None,
        constraint: str = None,
        pkeys: list[str] = None,
        row_buffer: int = 50000,
    ):
        """
        Upsert a specific size batch of data into PostgreSQL table.

        Params
        ------
        schema: Schema name
        table: Table name
        data: A list of dictionaries representing the data
        on_conflict_do_nothing: If True, the ON CONFLICT DO NOTHING method will be used
        on_conflict_do_update: If True, the ON CONFLICT DO UPDATE SET method will be used

        ! One of the following parameters must be provided if we want to use on conflict methods:
        constraint: The name of the constraint for the
            ON CONFLICT ON CONSTRAINT constraint DO UPDATE SET clause
        pkeys: The primary keys of the table wich will be used in the
            ON CONFLICT (pkeys) DO UPDATE SET clause

        row_buffer: The number of rows to be inserted in each batch
        """
        if not data:
            logger.info("No data to upsert")
            return

        query = PSQLQueryBuilder.build_upsert_query(
            schema=schema,
            table=table,
            columns=data[0].keys(),
            update_columns=update_columns,
            do_nothing=on_conflict_do_nothing,
            do_update=on_conflict_do_update,
            constraint=constraint,
            pkeys=pkeys,
        )

        self._connect()
        with psycopg2.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                execute_batch(cursor, query, data, page_size=row_buffer)
                conn.commit()
        self._disconnect()

        logger.info("Rows have been upserted: %(len)s", {"len": len(data)})

    def _open_sshtunnel(self):
        """Create SSH tunnel to the server."""
        self.ssh_tunnel = sshtunnel.SSHTunnelForwarder(**self.ssh_params)
        self.ssh_tunnel.start()

        self.conn_params["host"] = self.ssh_tunnel.local_bind_host
        self.conn_params["port"] = self.ssh_tunnel.local_bind_port

    def _connect(self):
        """Connect to the PSQL database."""
        try:
            if not self.conn_str:
                self._open_sshtunnel()
                self.conn_str = self.CONN_STR_PATTERN % self.conn_params

            self.engine = create_engine(self.conn_str)
        except Exception as e:
            logger.error("Failed to connect to the PSQL database\n%(error)s", extra={"error": e})
            self._disconnect()
            raise e

    def _disconnect(self):
        """Close SSH tunnel."""
        if self.ssh_tunnel:
            self.ssh_tunnel.stop()
