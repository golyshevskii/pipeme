import asyncio
from functools import wraps

from core.bot.menu import set_menu
from core.scripts.psql.manager import insert_tg_bot_user_access, select_tg_bot_user_access
from core.templates.bot.command import HAS_ACCESS_COMMANDS, NO_ACCESS_COMMANDS
from core.templates.bot.message import MESSAGE
from logs.logger import get_logger
from telegram import Update
from telegram.ext import ContextTypes

logger = get_logger(__name__)

USER = {}
USER_LOCK = asyncio.Lock()


async def on_no_user(update: Update):
    """Add new user to the database."""
    logger.debug(
        "New user %(username)s (%(user_id)s)",
        {"username": update.effective_user.username, "user_id": update.effective_user.id},
    )

    replay_only_faq = await set_menu(only_faq=True)
    await update.message.reply_markdown_v2(MESSAGE["need_access"], reply_markup=replay_only_faq)

    if not update.effective_user.is_bot:
        user_data = {"id": update.effective_user.id, "username": update.effective_user.username}

        await asyncio.get_event_loop().run_in_executor(None, insert_tg_bot_user_access, user_data)


async def on_no_access(update: Update):
    """Respond to users without access."""
    logger.warning(
        "Access denied for %(username)s (%(user_id)s)",
        {"username": update.effective_user.username, "user_id": update.effective_user.id},
    )

    replay_only_faq = await set_menu(only_faq=True)
    await update.message.reply_markdown_v2(MESSAGE["need_access"], reply_markup=replay_only_faq)


def access(func):
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = await asyncio.get_event_loop().run_in_executor(
            None, select_tg_bot_user_access, update.effective_user.id
        )
        await context.bot.set_my_commands(
            HAS_ACCESS_COMMANDS if not user.empty and user.has_access[0] else NO_ACCESS_COMMANDS
        )

        if user.empty:
            await on_no_user(update)
            return
        elif not user.has_access[0]:
            await on_no_access(update)
            return

        return await func(update, context, *args, **kwargs)

    return wrapped
