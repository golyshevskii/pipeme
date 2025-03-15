from config import PSQL_CONN_STR, TG_BOT_TOKEN
from halo import Halo


def check_tables():
    """Check tables."""
    from core.scripts.psql.client import PSQLClient
    from core.scripts.psql.maps import TABLE_MAP

    PSQL_CLIENT = PSQLClient(PSQL_CONN_STR)
    for _, data in TABLE_MAP.items():
        PSQL_CLIENT.execute(data["sql"])


def check_dependencies() -> bool:
    """Check dependencies."""
    spinner = Halo(text="Checking dependencies", spinner="dots")
    spinner.start()

    try:
        if not PSQL_CONN_STR:
            spinner.fail("PSQL_CONN_STR is not set. Please set it in the .env file.")
            return False

        if not TG_BOT_TOKEN:
            spinner.fail("TG_BOT_TOKEN is not set. Please set it in the .env file.")
            return False

        check_tables()

        spinner.succeed("All dependencies checked successfully")
        return True
    except Exception as e:
        spinner.fail(f"Error checking dependencies: {str(e)}")
        return False
    finally:
        spinner.stop()
