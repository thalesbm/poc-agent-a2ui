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
        
        # response = [{'beginRendering': {'surfaceId': 'default', 'root': 'root-column', 'styles': {'primaryColor': '#1E88E5', 'font': 'Roboto'}}}, {'surfaceUpdate': {'surfaceId': 'default', 'components': [{'id': 'root-column', 'component': {'Column': {'children': {'explicitList': ['title-heading', 'stocks-list']}}}}, {'id': 'title-heading', 'component': {'Text': {'usageHint': 'h1', 'text': {'path': 'title'}}}}, {'id': 'stocks-list', 'component': {'List': {'direction': 'vertical', 'children': {'template': {'componentId': 'stock-card-template', 'dataBinding': '/stocks'}}}}}, {'id': 'stock-card-template', 'component': {'Card': {'child': 'card-layout'}}}, {'id': 'card-layout', 'component': {'Column': {'children': {'explicitList': ['stock-header', 'stock-details']}}}}, {'id': 'stock-header', 'component': {'Row': {'children': {'explicitList': ['symbol-text', 'company-text', 'price-text']}}}}, {'id': 'symbol-text', 'weight': 1, 'component': {'Text': {'usageHint': 'h3', 'text': {'path': 'symbol'}}}}, {'id': 'company-text', 'weight': 2, 'component': {'Text': {'text': {'path': 'company'}}}}, {'id': 'price-text', 'weight': 1, 'component': {'Text': {'text': {'path': 'currentPrice', 'format': 'currency'}}}}, {'id': 'stock-details', 'component': {'Column': {'children': {'explicitList': ['recommendation-badge', 'sector-text', 'target-price-text']}}}}, {'id': 'recommendation-badge', 'component': {'Text': {'text': {'path': 'recommendation'}, 'style': {'color': '#4CAF50'}}}}, {'id': 'sector-text', 'component': {'Text': {'text': {'path': 'sector'}}}}, {'id': 'target-price-text', 'component': {'Text': {'text': {'path': 'targetPrice', 'format': 'currency'}}}}]}}, {'dataModelUpdate': {'surfaceId': 'default', 'path': '/', 'contents': [{'key': 'title', 'valueString': 'Investment Stock Recommendations'}, {'key': 'stocks', 'valueMap': [{'key': 'stock1', 'valueMap': [{'key': 'symbol', 'valueString': 'NVDA'}, {'key': 'company', 'valueString': 'NVIDIA Corporation'}, {'key': 'sector', 'valueString': 'Technology'}, {'key': 'currentPrice', 'valueNumber': 760.0}, {'key': 'recommendation', 'valueString': 'BUY'}, {'key': 'targetPrice', 'valueNumber': 900.0}]}, {'key': 'stock2', 'valueMap': [{'key': 'symbol', 'valueString': 'AAPL'}, {'key': 'company', 'valueString': 'Apple Inc.'}, {'key': 'sector', 'valueString': 'Technology'}, {'key': 'currentPrice', 'valueNumber': 175.5}, {'key': 'recommendation', 'valueString': 'BUY'}, {'key': 'targetPrice', 'valueNumber': 200.0}]}, {'key': 'stock3', 'valueMap': [{'key': 'symbol', 'valueString': 'MSFT'}, {'key': 'company', 'valueString': 'Microsoft Corporation'}, {'key': 'sector', 'valueString': 'Technology'}, {'key': 'currentPrice', 'valueNumber': 378.85}, {'key': 'recommendation', 'valueString': 'BUY'}, {'key': 'targetPrice', 'valueNumber': 420.0}]}, {'key': 'stock4', 'valueMap': [{'key': 'symbol', 'valueString': 'AMZN'}, {'key': 'company', 'valueString': 'Amazon.com, Inc.'}, {'key': 'sector', 'valueString': 'Consumer Discretionary'}, {'key': 'currentPrice', 'valueNumber': 135.0}, {'key': 'recommendation', 'valueString': 'BUY'}, {'key': 'targetPrice', 'valueNumber': 180.0}]}, {'key': 'stock5', 'valueMap': [{'key': 'symbol', 'valueString': 'JPM'}, {'key': 'company', 'valueString': 'JPMorgan Chase & Co.'}, {'key': 'sector', 'valueString': 'Financials'}, {'key': 'currentPrice', 'valueNumber': 150.25}, {'key': 'recommendation', 'valueString': 'HOLD'}, {'key': 'targetPrice', 'valueNumber': 170.0}]}]}]}}]

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

