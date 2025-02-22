from io import BytesIO
from typing import TYPE_CHECKING

from core.agent.models import Response, SuccessRequest
from core.agent.run import run_agent
from core.bot.menu import set_confirm_request_inline_menu, set_faq_inline_menu
from core.bot.wrapper import USER, USER_LOCK, access
from core.templates.bot.button import BUTTON_MAP
from core.templates.bot.message import MESSAGE
from logs.logger import get_logger
from telegram import InputMediaDocument, Update
from telegram.ext import CallbackContext, ContextTypes

if TYPE_CHECKING:
    from core.agent.models import Response

logger = get_logger(__name__)


@access
async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user input."""
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    logger.debug(
        "Handling %(username)s (%(user_id)s) user request...",
        {"username": username, "user_id": user_id},
    )

    async with USER_LOCK:
        if update.message.text:
            request = update.message.text
            USER[user_id] = {"request": request, "is_audio": False}
        elif update.message.voice:
            request = update.message.voice
            USER[user_id] = {"request": request, "is_audio": True}
        elif update.message.audio:
            request = update.message.audio
            USER[user_id] = {"request": request, "is_audio": True}
        else:
            logger.info(
                "User %(username)s (%(user_id)s) sent unknown message",
                {"username": username, "user_id": user_id},
            )
            await update.message.reply_markdown_v2(MESSAGE["unknown_message"])
            return

    reply_markup = await set_confirm_request_inline_menu()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MESSAGE["confirm_request"],
        parse_mode="MarkdownV2",
        reply_to_message_id=update.message.message_id,
        reply_markup=reply_markup,
    )


async def handle_confirm_request(update: Update, context: CallbackContext):
    """Handle request confirmation."""
    user_id = update.effective_user.id
    query = update.callback_query

    await query.answer()
    await query.edit_message_text(
        MESSAGE["run_request"],
        reply_markup=None,
        parse_mode="MarkdownV2",
    )

    try:
        await run_agent(user_id, context)
    except Exception as e:
        logger.error("Failed to run agent: %s", e)
        await query.edit_message_text(MESSAGE["run_agent_error"], parse_mode="MarkdownV2")
        return

    data: Response = USER[user_id]["data"]

    if isinstance(data, SuccessRequest):
        sql_bytes = BytesIO(data.sql.encode("utf-8"))
        sql_bytes.name = f"sql_{user_id}.sql"

        yml_bytes = BytesIO(data.yml.encode("utf-8"))
        yml_bytes.name = f"yml_{user_id}.yml"

        media = [
            InputMediaDocument(media=sql_bytes),
            InputMediaDocument(media=yml_bytes),
        ]

        await query.edit_message_text(data.explanation, reply_markup=None)
        await context.bot.send_media_group(chat_id=user_id, media=media)
    else:
        await query.edit_message_text(text=data.error_message, reply_markup=None)


async def handle_reset_request(update: Update, context: CallbackContext):
    """Handle request reset."""
    query = update.callback_query
    await query.answer()

    try:
        await query.delete_message()
    except Exception as e:
        logger.error("Can't delete message: %s", e)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=MESSAGE["reset_request"], parse_mode="MarkdownV2"
    )


async def handle_faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle FAQ request."""
    reply_markup = await set_faq_inline_menu()
    await update.message.reply_markdown_v2(MESSAGE["faq"], reply_markup=reply_markup)
    return


async def handle_faq_question(update: Update, context: CallbackContext):
    """Handle FAQ question."""
    query = update.callback_query
    await query.answer()

    question = query.data
    await query.edit_message_text(
        f">{BUTTON_MAP[question]}\n\n\n{MESSAGE[question]}", reply_markup=None, parse_mode="MarkdownV2"
    )
