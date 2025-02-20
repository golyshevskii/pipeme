from config import OPENAI_API_KEY, OPENAI_API_URL
from core.agent.models import InvalidRequest, Response
from core.agent.prompts import DB_SCHEMA, REMINDER, SQL_EXAMPLES, WHAT_TO_DO, WHO_ARE_YOU, YML_EXAMPLES
from logs.logger import get_logger
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

logger = get_logger(__name__)

OPENAI_MODEL = OpenAIModel("gpt-4o", base_url=OPENAI_API_URL, api_key=OPENAI_API_KEY)
AGENT: Agent[Response] = Agent(
    model=OPENAI_MODEL,
    result_type=Response,
)


@AGENT.system_prompt
async def system_prompt() -> str:
    """
    Build system prompt.

    Fields
    ------
    who_am_i: Explaining who an agent is and what he must do
    db_schema: Database schema from where an agent will get data about entities
    yml_examples: Examples how to generate YAML files
    sql_examples: Examples how to generate SQL queries
    what_to_do: What an agent must do according to the request
    """
    return f"""
    ### Who are you:
    {WHO_ARE_YOU}

    ### Database schema:
    {DB_SCHEMA}

    ### YAML examples (keep to the format):
    {YML_EXAMPLES}

    ### SQL examples (keep to the format):
    {SQL_EXAMPLES}

    ### What to do:
    {WHAT_TO_DO}

    ### Reminder:
    {REMINDER}
    """


@AGENT.result_validator
async def validate_result(result: Response) -> Response:
    """Validate agent result."""
    if isinstance(result, InvalidRequest):
        return result
    return result
