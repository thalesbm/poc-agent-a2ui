"""
Simple API to expose the agent's invoke method.
Demo/POC use case for investment recommendations.
"""
import uvicorn

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Union, Any

from llm.client.openai import OpenAIClient
from llm.client.openai_key import OpenAIKey
from logger.logger_config import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Investment Recommendations API",
    description="API for investment stock recommendations using A2UI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InvestmentResponse(BaseModel):
    """Response model for investment recommendations."""
    success: bool
    data: Optional[Union[dict, list]] = None
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
        client = OpenAIClient(api_key=OpenAIKey().get_openai_key())
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
    uvicorn.run(app, host="localhost", port=8000)

