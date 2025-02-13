from core.bot.wrapper import access
from core.templates.bot.message import MESSAGE
from logs.logger import get_logger
from telegram import Update
from telegram.ext import ContextTypes

logger = get_logger(__name__)


@access
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responds to /start command"""
    user_id = update.effective_user.id
    username = update.effective_user.username
    logger.debug(f"User {username} ({user_id}) started the bot")

    await update.message.reply_markdown_v2(MESSAGE["start"])
