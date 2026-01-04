"""
Simple prompt for investment stock recommendations.
Demo/POC use case.
"""

from llm.prompt.json_schema import STOCK_INVESTMENT_RECOMMENDATIONS_SCHEMA

def get_investment_prompt() -> str:
    """
    Constructs the prompt for investment stock recommendations.
    
    Returns:
        A formatted string to be used as the system prompt for the LLM.
    """
    
    return f"""
    You are a helpful investment advisor assistant. Your final output MUST be a JSON object, according to the JSON SCHEMA provided below.
    
    To generate the response, you MUST follow these rules:
    1. The JSON object MUST be in JSON format, according to the JSON SCHEMA provided below.
    2. Use the investment stocks data you have already received from the `get_investment_stocks` api to populate the `data` array.
    3. The JSON object MUST contain a `footer` property with a string description of the recommendations.
    4. The JSON object MUST contain title of the recommendations and description of the recommendations.
    5. Always format prices as currency (e.g., $175.50).
    
    ---BEGIN JSON SCHEMA---
    {STOCK_INVESTMENT_RECOMMENDATIONS_SCHEMA}
    ---END JSON SCHEMA---
    """

