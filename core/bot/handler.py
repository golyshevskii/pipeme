from io import BytesIO
from typing import TYPE_CHECKING

from core.agent.models import Response
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
    request = update.message.text
    logger.debug(
        "Handling %(username)s (%(user_id)s) user input text: %(text)s",
        {"username": username, "user_id": user_id, "text": request},
    )

    async with USER_LOCK:
        USER[user_id] = {"request": request}

    reply_markup = await set_confirm_request_inline_menu()
    await update.message.reply_markdown_v2(
        f"{MESSAGE['confirm_request']}\n\n```\n{request}\n```", reply_markup=reply_markup
    )


async def handle_faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle FAQ request."""
    reply_markup = await set_faq_inline_menu()
    await update.message.reply_markdown_v2(MESSAGE["faq"], reply_markup=reply_markup)
    return


async def handle_confirm_request(update: Update, context: CallbackContext):
    """Handle request confirmation."""
    user_id = update.effective_user.id
    query = update.callback_query

    await query.answer()
    await query.edit_message_text(
        f"```\n{USER[user_id]['request']}\n```\n\n{MESSAGE['run_request']}",
        reply_markup=None,
        parse_mode="MarkdownV2",
    )

    await run_agent(user_id)
    data: Response = USER[user_id]["data"]

    sql_bytes = BytesIO(data.sql.encode("utf-8"))
    sql_bytes.name = f"sql_{user_id}.sql"
    yml_bytes = BytesIO(data.yml.encode("utf-8"))
    yml_bytes.name = f"yml_{user_id}.yml"

    media = [InputMediaDocument(media=sql_bytes), InputMediaDocument(media=yml_bytes)]

    await query.edit_message_text(data.explanation, reply_markup=None)
    await context.bot.send_media_group(chat_id=user_id, media=media)


async def handle_reset_request(update: Update, context: CallbackContext):
    """Handle request reset."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(MESSAGE["reset_request"], reply_markup=None, parse_mode="MarkdownV2")


async def handle_faq_question(update: Update, context: CallbackContext):
    """Handle FAQ question."""
    query = update.callback_query
    await query.answer()

    question = query.data
    logger.debug(
        "User %(username)s (%(user_id)s) asked: %(question)s",
        {
            "username": update.effective_user.username,
            "user_id": update.effective_user.id,
            "question": question,
        },
    )
    await query.edit_message_text(
        f">{BUTTON_MAP[question]}\n\n\n{MESSAGE[question]}", reply_markup=None, parse_mode="MarkdownV2"
    )
