from io import BytesIO

from config import OPENAI_API_KEY, OPENAI_API_URL
from core.bot.wrapper import USER
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
