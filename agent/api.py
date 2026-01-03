"""
Simple API to expose the agent's invoke method.
Demo/POC use case for investment recommendations.
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from llm.client.openai import OpenAIClient
from llm.client.openai_key import OpenAIKey
from logger.logger_config import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Investment Recommendations API",
    description="API for investment stock recommendations using A2UI",
    version="1.0.0"
)


class InvestmentResponse(BaseModel):
    """Response model for investment recommendations."""
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None

@app.get("/", response_model=InvestmentResponse)
async def invoke_agent(
    query: str = Query(
        default="Recommend 5 stocks to invest this year.",
        description="Query string for investment recommendations"
    )
):
    """
    Invokes the agent to get investment recommendations.
    
    Args:
        query: Query string for investment recommendations
        
    Returns:
        InvestmentResponse with the A2UI JSON response
    """
    try:
        # logger.info(f"Received request: {query}")
        
        # Get API key from environment
        api_key = OpenAIKey().get_openai_key()
        
        # Create client and invoke
        client = OpenAIClient(api_key=api_key)
        response = client.invoke(query=query)
        
        logger.info("Successfully generated investment recommendations")
        
        return InvestmentResponse(
            success=True,
            data=response
        )
        
    except Exception as e:
        logger.error(f"Error in invoke_agent: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

