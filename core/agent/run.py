from config import OPENAI_API_KEY, OPENAI_API_URL
from core.agent.models import Response
from core.agent.utils import transcribe_audio
from core.bot.wrapper import USER, USER_LOCK
from logs.logger import get_logger
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from telegram.ext import CallbackContext

logger = get_logger(__name__)


OPENAI_MODEL = OpenAIModel("gpt-4o", base_url=OPENAI_API_URL, api_key=OPENAI_API_KEY)
AGENT: Agent[Response] = Agent(
    model=OPENAI_MODEL,
    result_type=Response,
)


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

    # TODO: Add embedding to the request & find the relevant context in QDRANT.
    # TODO: Add the context to the system prompt.

    logger.info("Starting the agent for the user %(user_id)s", {"user_id": user_id})
    result = await AGENT.run(request)

    async with USER_LOCK:
        USER[user_id]["result"] = result
        USER[user_id]["data"] = result.data

    logger.info(
        "The agent executed successfully for user %(user_id)s. Result: %(result)s",
        {"user_id": user_id, "result": result.data},
    )
