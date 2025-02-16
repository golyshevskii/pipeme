from core.bot.menu import set_menu
from core.bot.wrapper import USER, USER_LOCK, access
from core.templates.bot.message import MESSAGE
from logs.logger import get_logger
from telegram import Update
from telegram.ext import ContextTypes

logger = get_logger(__name__)


@access
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Respond to /start command."""
    user_id = update.effective_user.id
    username = update.effective_user.username
    logger.debug(
        "User %(username)s (%(user_id)s) started the bot", {"username": username, "user_id": user_id}
    )

    async with USER_LOCK:
        USER[user_id] = {}

    reply_markup = await set_menu()
    await update.message.reply_markdown_v2(MESSAGE["start"], reply_markup=reply_markup)
