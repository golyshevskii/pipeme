from config import TG_BOT_TOKEN
from core.bot.command import start
from core.bot.handler import (
    handle_confirm_request,
    handle_faq,
    handle_faq_question,
    handle_input,
    handle_reset_request,
)
from logs.logger import get_logger
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, filters

logger = get_logger(__name__)


def run():
    """Run the main logic of the Bot."""
    logger.debug("BEGIN")
    app = ApplicationBuilder().token(TG_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("(?i)^faq$"), handle_faq))
    app.add_handler(
        MessageHandler((filters.TEXT | filters.VOICE | filters.AUDIO) & ~filters.COMMAND, handle_input)
    )
    app.add_handler(CallbackQueryHandler(handle_faq_question, pattern="^faq_"))
    app.add_handler(CallbackQueryHandler(handle_confirm_request, pattern="^confirm_request$"))
    app.add_handler(CallbackQueryHandler(handle_reset_request, pattern="^reset_request$"))

    app.run_polling(drop_pending_updates=True)
    logger.debug("END")


if __name__ == "__main__":
    run()
