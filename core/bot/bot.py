from config import G8AGENT_BOT_TOKEN
from core.bot.command import start
from core.bot.handler import handle_input
from logs.logger import get_logger
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

logger = get_logger(__name__)


def run():
    """Runs the main logic of the Bot"""
    logger.debug("BEGIN")
    app = ApplicationBuilder().token(G8AGENT_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))

    app.run_polling(drop_pending_updates=True)
    logger.debug("END")


if __name__ == "__main__":
    run()
