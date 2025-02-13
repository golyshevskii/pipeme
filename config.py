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
G8AGENT_BOT_TOKEN = os.getenv("ENV_VAR_G8AGENT_BOT_TOKEN")
G8AGENT_BOT_URL = "https://t.me/G8AgentBot"
