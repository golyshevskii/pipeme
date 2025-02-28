from config import OPENAI_API_KEY, OPENAI_API_URL
from core.agent.models import InvalidRequest, Response
from core.agent.prompts import (
    ADDITIONAL_INFORMATION,
    DATA_CONTEXT,
    SQL_EXAMPLES,
    WARNINGS,
    WHAT_TO_DO,
    WHO_ARE_YOU,
    YML_EXAMPLES,
)
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
    # WHO ARE YOU
    {WHO_ARE_YOU}

    # WHAT TO DO
    {WHAT_TO_DO}

    # EXAMPLES
    - YAML:
    {YML_EXAMPLES}

    - SQL:
    {SQL_EXAMPLES}

    # WARNINGS
    {WARNINGS}

    --

    # DATA CONTEXT
    {DATA_CONTEXT}

    # ADDITIONAL INFORMATION
    {ADDITIONAL_INFORMATION}
    """


@AGENT.result_validator
async def validate_result(result: Response) -> Response:
    """Validate agent result."""
    if isinstance(result, InvalidRequest):
        return result
    return result
