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
    async with USER_LOCK:
        USER[user_id]["result"] = await AGENT.run(USER[user_id]["text"])

    logger.debug("Agent result: %(result)s", {"result": USER[user_id]["result"]})
