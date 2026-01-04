import os

from dotenv import load_dotenv

from logger.logger_config import get_logger

logger = get_logger(__name__)

load_dotenv()

class OpenAIKey:
    """Class responsible for managing the OpenAI API key."""

    def get_openai_key(self) -> str:
        """
        Gets the OpenAI API key.
        """
        api_key = os.getenv("OPENAI_API_KEY")

        if api_key:
            logger.info("OpenAI API key loaded successfully")
        else:
            logger.warning("OpenAI API key not found!")

        return api_key
