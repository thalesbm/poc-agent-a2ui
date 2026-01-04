"""
A2UI examples for investment stocks data.
Based on Google's A2UI protocol.
"""

INVESTMENT_STOCKS_UI_EXAMPLES = """
---BEGIN SINGLE_COLUMN_LIST_EXAMPLE---
[
  {{ "beginRendering": {{ "surfaceId": "default", "root": "root-column", "styles": {{ "primaryColor": "#1E88E5", "font": "Roboto" }} }} }},
  {{ "surfaceUpdate": {{
    "surfaceId": "default",
    "components": [
      {{ "id": "root-column", "component": {{ "Column": {{ "children": {{ "explicitList": ["title-heading", "stocks-list"] }} }} }} }},
      {{ "id": "title-heading", "component": {{ "Text": {{ "usageHint": "h1", "text": {{ "path": "title" }} }} }} }},
      {{ "id": "stocks-list", "component": {{ "List": {{ "direction": "vertical", "children": {{ "template": {{ "componentId": "stock-card-template", "dataBinding": "/stocks" }} }} }} }} }},
      {{ "id": "stock-card-template", "component": {{ "Card": {{ "child": "card-layout" }} }} }},
      {{ "id": "card-layout", "component": {{ "Column": {{ "children": {{ "explicitList": ["stock-header"] }} }} }} }},
      {{ "id": "stock-header", "component": {{ "Row": {{ "children": {{ "explicitList": ["symbol-text", "company-text", "price-text"] }} }} }} }},
      {{ "id": "symbol-text", "weight": 1, "component": {{ "Text": {{ "usageHint": "h3", "text": {{ "path": "symbol" }} }} }} }},
      {{ "id": "company-text", "weight": 2, "component": {{ "Text": {{ "text": {{ "path": "company" }} }} }} }},
      {{ "id": "price-text", "weight": 1, "component": {{ "Text": {{ "text": {{ "path": "currentPrice", "format": "currency" }} }} }} }},
      {{ "id": "recommendation-badge", "component": {{ "Text": {{ "text": {{ "path": "recommendation" }}, "style": {{ "color": "#4CAF50" }} }} }} }},
      {{ "id": "sector-text", "component": {{ "Text": {{ "text": {{ "path": "sector" }} }} }} }},
      {{ "id": "target-price-text", "component": {{ "Text": {{ "text": {{ "path": "targetPrice", "format": "currency" }} }} }} }},
    ]
  }} }},
  {{ "dataModelUpdate": {{
    "surfaceId": "default",
    "path": "/",
    "contents": [
      {{ "key": "title", "valueString": "Investment Stock Recommendations" }},
      {{ "key": "stocks", "valueMap": [
        {{ "key": "stock1", "valueMap": [
          {{ "key": "symbol", "valueString": "AAPL" }},
          {{ "key": "company", "valueString": "Apple Inc." }},
          {{ "key": "sector", "valueString": "Technology" }},
          {{ "key": "currentPrice", "valueNumber": 175.50 }},
          {{ "key": "recommendation", "valueString": "BUY" }},
          {{ "key": "targetPrice", "valueNumber": 200.00 }}
        ] }},
        {{ "key": "stock2", "valueMap": [
          {{ "key": "symbol", "valueString": "MSFT" }},
          {{ "key": "company", "valueString": "Microsoft Corporation" }},
          {{ "key": "sector", "valueString": "Technology" }},
          {{ "key": "currentPrice", "valueNumber": 378.85 }},
          {{ "key": "recommendation", "valueString": "BUY" }},
          {{ "key": "targetPrice", "valueNumber": 420.00 }}
        ] }}
      ] }}
    ]
  }} }}
]
---END SINGLE_COLUMN_LIST_EXAMPLE---

"""

