import json
import jsonschema
import re

from langchain_openai.chat_models import ChatOpenAI

from openai import OpenAIError

from a2ui.a2ui_schema import A2UI_SCHEMA
from llm.prompt.prompt import get_prompt
from logger.logger_config import get_logger

logger = get_logger(__name__)

class OpenAIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def invoke(self) -> dict | None:
        """
        Invokes the OpenAI API with the prompt and returns the response.

        Returns:
            A tuple containing the parsed JSON data and the text part.
        """
        logger.info("Invoking OpenAI")

        try:
            chat_openai = ChatOpenAI(
                model="gpt-5-mini-2025-08-07",
                api_key=self.api_key,
            )
            response = chat_openai.invoke(get_prompt() + "\n\nTop 5 Chinese restaurants in New York.")
        except OpenAIError as e:
            logger.error(f"Error invoking OpenAI: {e}")
            raise e

        logger.info(f"Response: {response.content}")

        logger.info("Validating response against A2UI schema")
        try:
            parsed_json_data, text_part = self._extract_json(response.content)

            jsonschema.validate(instance=parsed_json_data, schema=json.loads(A2UI_SCHEMA))
            logger.info("Response validated against A2UI schema")

            return parsed_json_data
        except jsonschema.exceptions.ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise e

    def _extract_json(self, text: str) -> tuple[dict, str]:
        """
        Extracts the text part and the JSON part from the response.

        Args:
            text: The response from the OpenAI API.

        Returns:
            A tuple containing the parsed JSON data and the text part.
        """
        text_part, json_string = text.split(
            "---a2ui_JSON---", 1
        )

        json_string_cleaned = (
            json_string.strip().lstrip("```json").rstrip("```").strip()
        )

        parsed_json_data = json.loads(json_string_cleaned)

        return parsed_json_data, text_part
