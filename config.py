import os
from datetime import datetime, timezone
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

# SYSTEM
TODAY = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
ADMIN_EMAIL = os.getenv("ENV_VAR_ADMIN_EMAIL")

# DATA
LOG_PATH = f"{BASE_DIR}/logs/"
DATA_PATH = f"{BASE_DIR}/data/"

# Telegram
TG_BOT_ADMIN = "golyshevskii"
TG_BOT_TOKEN = os.getenv("ENV_VAR_TG_BOT_TOKEN")
TG_BOT_URL = "https://t.me/pipeme_bot"

# PSQL
PSQL_CONN_STR = os.getenv("ENV_VAR_PSQL_CONN_STR")

# OPENAI
OPENAI_API_KEY = os.getenv("ENV_VAR_OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1"