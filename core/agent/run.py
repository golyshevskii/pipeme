from core.agent.agent import AGENT
from core.bot.wrapper import USER, USER_LOCK
from logs.logger import get_logger

logger = get_logger(__name__)


async def run_agent(user_id: int) -> None:
    """
    Run the agent.

    Params
    ------
    user_id: The ID of the user
    text: The user input
    """
    logger.debug("Agent running for user: %(user_id)s", {"user_id": user_id})

    async with USER_LOCK:
        result = await AGENT.run(USER[user_id]["request"])

        USER[user_id]["result"] = result
        USER[user_id]["data"] = result.data

    logger.info("Agent has been run successfully for user: %(user_id)s.", {"user_id": user_id})
