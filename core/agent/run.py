from core.agent.agent import AGENT
from core.agent.utils import transcribe_audio
from core.bot.wrapper import USER, USER_LOCK
from logs.logger import get_logger
from telegram.ext import CallbackContext

logger = get_logger(__name__)


async def run_agent(user_id: int, context: CallbackContext) -> None:
    """
    Run the agent.

    Params
    ------
    user_id: The ID of the user
    context: The context of the bot
    """
    if USER[user_id].get("is_audio"):
        request = await transcribe_audio(user_id, context)
    else:
        request = USER[user_id]["request"]

    logger.info("Starting the agent for the user %(user_id)s", {"user_id": user_id})
    result = await AGENT.run(request)

    async with USER_LOCK:
        USER[user_id]["result"] = result
        USER[user_id]["data"] = result.data

    logger.info(
        "The agent executed successfully for user %(user_id)s. Result: %(result)s",
        {"user_id": user_id, "result": result.data},
    )
