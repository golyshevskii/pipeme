from io import BytesIO

from config import OPENAI_API_KEY, OPENAI_API_URL
from core.agent.prompts import (
    ADDITIONAL_INFORMATION,
    SQL_EXAMPLES,
    WARNINGS,
    WHAT_TO_DO,
    WHO_ARE_YOU,
    YML_EXAMPLES,
)
from core.bot.wrapper import USER
from core.scripts.embedding.manager import EMBEDDING_MANAGER
from core.scripts.qdrant.client import AQDRANT_CLIENT
from logs.logger import get_logger
from openai import OpenAI
from telegram.ext import CallbackContext

logger = get_logger(__name__)


async def transcribe_audio(user_id: int, context: CallbackContext) -> str:
    """Transcribe user voice or audio file."""
    logger.debug("Transcribing audio message for user %(user_id)s", {"user_id": user_id})

    file_info = await context.bot.get_file(USER[user_id]["request"].file_id)
    audio_data = await file_info.download_as_bytearray()

    audio = BytesIO(audio_data)
    audio.name = f"audio_{user_id}.ogg"

    client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_URL)
    transcription = client.audio.transcriptions.create(model="whisper-1", file=audio)

    logger.debug(
        "Transcription for user %(user_id)s: %(transcription)s",
        {"user_id": user_id, "transcription": transcription.text},
    )
    return transcription.text


async def find_request_context(user_id: int, request: str, top_n: int = 3) -> str:
    """
    Find the context for the request.

    Params
    ------
    user_id: The ID of the user
    request: The request to find the context for
    top_n: The number of top relevant context to return
    """
    vector = await EMBEDDING_MANAGER.vectorize(request)
    context = await AQDRANT_CLIENT.search(
        collection_name="pipeme",
        query_vector=vector,
        limit=top_n,
    )
    logger.debug(
        "Context for the user %(user_id)s request: %(context)s", {"user_id": user_id, "context": context}
    )
    return context


async def build_system_prompt(context: str) -> str:
    """
    Build system prompt.

    Fields
    ------
    WHO_ARE_YOU: Explaining who an agent is and what he must do
    WHAT_TO_DO: What an agent must do according to the request
    YML_EXAMPLES: Examples how to generate YAML files
    SQL_EXAMPLES: Examples how to generate SQL queries
    WARNINGS: Warnings about how to generate responses
    context: Context for the request that was found in the vector database
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

    # CONTEXT FOR THE REQUEST
    {context}

    # ADDITIONAL INFORMATION
    {ADDITIONAL_INFORMATION}
    """
