import json
import jsonschema

from langchain_openai.chat_models import ChatOpenAI

from llm.prompt.json_schema import STOCK_INVESTMENT_RECOMMENDATIONS_SCHEMA
from llm.prompt.investment_prompt import get_investment_prompt
from logger.logger_config import get_logger

logger = get_logger(__name__)

class OpenAIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def invoke(self, query: str = "Recommend 5 stocks to invest this year.") -> str:
        """
        Invokes the OpenAI API with the prompt and returns the response.

        Args:
            query: Optional query string to append to the prompt.

        Returns:
            A tuple containing the parsed JSON data and the text part.
        """

        logger.info("Invoking OpenAI")

        chat_openai = ChatOpenAI(
            model="gpt-5-mini-2025-08-07",
            api_key=self.api_key,
        )
        response = chat_openai.invoke(get_investment_prompt() + f"\n\n{query}")
        
        try:
            logger.info("Validating response against JSON schema")

            schema = json.loads(STOCK_INVESTMENT_RECOMMENDATIONS_SCHEMA)

            jsonschema.validate(instance=json.loads(response.content), schema=schema)

            logger.info("Response validated against JSON schema")

            return response.content
        except Exception as e:
            logger.error(f"Validation error: {e}")
            raise e
