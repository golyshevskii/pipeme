import asyncio
from functools import wraps

from core.scripts.psql.manager import insert_user, select_user
from core.templates.bot.message import MESSAGE
from logs.logger import get_logger
from telegram import Update
from telegram.ext import ContextTypes

logger = get_logger(__name__)


async def on_no_user(update: Update):
    """Adds new user to the database"""
    logger.debug(f"New user {update.effective_user.username} ({update.effective_user.id})")

    await update.message.reply_markdown_v2(MESSAGE["need_access"])
    if not update.effective_user.is_bot:
        user_data = {"id": update.effective_user.id, "username": update.effective_user.username}

        await asyncio.get_event_loop().run_in_executor(None, insert_user, user_data)


async def on_no_access(update: Update):
    """Responds to users without access"""
    logger.warning(f"Access denied for {update.effective_user.username} ({update.effective_user.id})")

    await update.message.reply_markdown_v2(MESSAGE["need_access"])


def access(func):
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = await asyncio.get_event_loop().run_in_executor(None, select_user, update.effective_user.id)

        if user.empty:
            await on_no_user(update)
            return
        elif not user.has_access[0]:
            await on_no_access(update)
            return

        return await func(update, context, *args, **kwargs)

    return wrapped
