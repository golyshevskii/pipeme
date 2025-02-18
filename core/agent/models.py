from typing import Annotated, Union

from annotated_types import MinLen
from pydantic import BaseModel, Field
from typing_extensions import TypeAlias


class SuccessRequest(BaseModel):
    """
    Response when SQL could be successfully generated.

    Fields
    ------
    sql: SQL query
    yml: YAML file
    explanation: Explanation of the YAML and SQL output
    """

    sql: Annotated[str, MinLen(1)]
    yml: Annotated[str, MinLen(1)]
    explanation: str = Field("", description="Explanation of the YAML and SQL output")


class InvalidRequest(BaseModel):
    """
    Response the user input didn't include enough information to generate YAML or SQL.

    Fields
    ------
    error_message: Error message
    """

    error_message: str


Response: TypeAlias = Union[SuccessRequest, InvalidRequest]
