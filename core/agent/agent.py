from typing import Annotated, Union

from annotated_types import MinLen
from logs.logger import get_logger
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing_extensions import TypeAlias

logger = get_logger(__name__)


class Success(BaseModel):
    """Response when SQL could be successfully generated."""

    sql_query: Annotated[str, MinLen(1)]
    explanation: str = Field("", description="Explanation of the SQL query, as markdown")


class InvalidRequest(BaseModel):
    """Response the user input didn't include enough information to generate SQL."""

    error_message: str


Response: TypeAlias = Union[Success, InvalidRequest]
AGENT: Agent[Response] = Agent(
    "gpt4-o1-mini",
    result_type=Response,
)


@AGENT.system_prompt
async def build_system_prompt(
    who_am_i: str, db_schema: str, yml_examples: str, sql_examples: str, what_to_do: str
) -> str:
    """
    Build system prompt.

    Params
    ------
    who_am_i: Explaining who an agent is and what he must do
    db_schema: Database schema from where an agent will get data about entities
    yml_examples: Examples how to generate YAML files
    sql_examples: Examples how to generate SQL queries
    what_to_do: What an agent must do according to the request
    """
    return f"""
    ### Who are you:
    {who_am_i}

    ### Database schema:
    {db_schema}

    ### YAML Examples:
    {yml_examples}

    ### SQL Examples:
    {sql_examples}

    ### What to do:
    {what_to_do}
    """


@AGENT.result_validator
async def validate_result(result: Response) -> Response:
    pass
