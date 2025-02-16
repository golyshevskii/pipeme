from core.bot.menu import set_confirm_request_inline_menu, set_faq_inline_menu
from core.bot.wrapper import USER, USER_LOCK, access
from core.templates.bot.button import BUTTON_MAP
from core.templates.bot.message import MESSAGE
from logs.logger import get_logger
from telegram import Update
from telegram.ext import CallbackContext, ContextTypes

logger = get_logger(__name__)


@access
async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user input."""
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    text = update.message.text
    logger.debug(
        "Handling %(username)s (%(user_id)s) user input text: %(text)s",
        {"username": username, "user_id": user_id, "text": text},
    )

    async with USER_LOCK:
        USER[user_id] = {"text": text}

    reply_markup = await set_confirm_request_inline_menu()
    await update.message.reply_markdown_v2(
        f"{MESSAGE['confirm_request']}\n\n```\n{text}\n```", reply_markup=reply_markup
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
        f"```\n{USER[user_id]['text']}\n```\n\n{MESSAGE['run_request']}",
        reply_markup=None,
        parse_mode="MarkdownV2",
    )

    # TODO: start process


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
