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
      {{ "id": "card-layout", "component": {{ "Column": {{ "children": {{ "explicitList": ["stock-header", "stock-details", "stock-actions"] }} }} }} }},
      {{ "id": "stock-header", "component": {{ "Row": {{ "children": {{ "explicitList": ["symbol-text", "company-text", "price-text"] }} }} }} }},
      {{ "id": "symbol-text", "weight": 1, "component": {{ "Text": {{ "usageHint": "h3", "text": {{ "path": "symbol" }} }} }} }},
      {{ "id": "company-text", "weight": 2, "component": {{ "Text": {{ "text": {{ "path": "company" }} }} }} }},
      {{ "id": "price-text", "weight": 1, "component": {{ "Text": {{ "text": {{ "path": "currentPrice", "format": "currency" }} }} }} }},
      {{ "id": "stock-details", "component": {{ "Column": {{ "children": {{ "explicitList": ["recommendation-badge", "sector-text", "target-price-text"] }} }} }} }},
      {{ "id": "recommendation-badge", "component": {{ "Text": {{ "text": {{ "path": "recommendation" }}, "style": {{ "color": "#4CAF50" }} }} }} }},
      {{ "id": "sector-text", "component": {{ "Text": {{ "text": {{ "path": "sector" }} }} }} }},
      {{ "id": "target-price-text", "component": {{ "Text": {{ "text": {{ "path": "targetPrice", "format": "currency" }} }} }} }},
      {{ "id": "stock-actions", "component": {{ "Row": {{ "children": {{ "explicitList": ["view-details-button", "invest-button"] }} }} }} }},
      {{ "id": "view-details-button", "weight": 1, "component": {{ "Button": {{ "child": "view-details-text", "action": {{ "name": "view_stock_details", "context": [ {{ "key": "symbol", "value": {{ "path": "symbol" }} }}, {{ "key": "company", "value": {{ "path": "company" }} }}, {{ "key": "currentPrice", "value": {{ "path": "currentPrice" }} }}, {{ "key": "targetPrice", "value": {{ "path": "targetPrice" }} }} ] }} }} }} }},
      {{ "id": "view-details-text", "component": {{ "Text": {{ "text": {{ "literalString": "View Details" }} }} }} }},
      {{ "id": "invest-button", "weight": 1, "component": {{ "Button": {{ "child": "invest-text", "primary": true, "action": {{ "name": "invest_in_stock", "context": [ {{ "key": "symbol", "value": {{ "path": "symbol" }} }}, {{ "key": "company", "value": {{ "path": "company" }} }}, {{ "key": "currentPrice", "value": {{ "path": "currentPrice" }} }}, {{ "key": "recommendation", "value": {{ "path": "recommendation" }} }} ] }} }} }} }},
      {{ "id": "invest-text", "component": {{ "Text": {{ "text": {{ "literalString": "Invest" }} }} }} }}
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

---BEGIN DETAILED_CARD_EXAMPLE---
[
  {{ "beginRendering": {{ "surfaceId": "default", "root": "root-column", "styles": {{ "primaryColor": "#1E88E5", "font": "Roboto" }} }} }},
  {{ "surfaceUpdate": {{
    "surfaceId": "default",
    "components": [
      {{ "id": "root-column", "component": {{ "Column": {{ "children": {{ "explicitList": ["title-heading", "detailed-stock-card"] }} }} }} }},
      {{ "id": "title-heading", "component": {{ "Text": {{ "usageHint": "h1", "text": {{ "path": "title" }} }} }} }},
      {{ "id": "detailed-stock-card", "component": {{ "Card": {{ "child": "detailed-card-layout" }} }} }},
      {{ "id": "detailed-card-layout", "component": {{ "Column": {{ "children": {{ "explicitList": ["stock-header-section", "price-section", "recommendation-section", "details-section", "action-section"] }} }} }} }},
      {{ "id": "stock-header-section", "component": {{ "Row": {{ "children": {{ "explicitList": ["symbol-large", "company-name"] }} }} }} }},
      {{ "id": "symbol-large", "weight": 1, "component": {{ "Text": {{ "usageHint": "h2", "text": {{ "path": "/stock/symbol" }} }} }} }},
      {{ "id": "company-name", "weight": 2, "component": {{ "Text": {{ "usageHint": "h3", "text": {{ "path": "/stock/company" }} }} }} }},
      {{ "id": "price-section", "component": {{ "Row": {{ "children": {{ "explicitList": ["current-price", "target-price"] }} }} }} }},
      {{ "id": "current-price", "weight": 1, "component": {{ "Text": {{ "text": {{ "path": "/stock/currentPrice", "format": "currency" }} }} }} }},
      {{ "id": "target-price", "weight": 1, "component": {{ "Text": {{ "text": {{ "path": "/stock/targetPrice", "format": "currency" }} }} }} }},
      {{ "id": "recommendation-section", "component": {{ "Column": {{ "children": {{ "explicitList": ["recommendation-badge-large"] }} }} }} }},
      {{ "id": "recommendation-badge-large", "component": {{ "Text": {{ "text": {{ "path": "/stock/recommendation" }} }} }} }},
      {{ "id": "details-section", "component": {{ "Column": {{ "children": {{ "explicitList": ["sector-text"] }} }} }} }},
      {{ "id": "sector-text", "component": {{ "Text": {{ "text": {{ "path": "/stock/sector" }} }} }} }},
      {{ "id": "action-section", "component": {{ "Row": {{ "children": {{ "explicitList": ["invest-button-large"] }} }} }} }},
      {{ "id": "invest-button-large", "component": {{ "Button": {{ "child": "invest-text-large", "primary": true, "action": {{ "name": "invest_in_stock", "context": [ {{ "key": "symbol", "value": {{ "path": "/stock/symbol" }} }}, {{ "key": "company", "value": {{ "path": "/stock/company" }} }}, {{ "key": "currentPrice", "value": {{ "path": "/stock/currentPrice" }} }}, {{ "key": "recommendation", "value": {{ "path": "/stock/recommendation" }} }} ] }} }} }} }},
      {{ "id": "invest-text-large", "component": {{ "Text": {{ "text": {{ "literalString": "Invest Now" }} }} }} }}
    ]
  }} }},
  {{ "dataModelUpdate": {{
    "surfaceId": "default",
    "path": "/",
    "contents": [
      {{ "key": "title", "valueString": "Stock Details" }},
      {{ "key": "stock", "valueMap": [
        {{ "key": "symbol", "valueString": "AAPL" }},
        {{ "key": "company", "valueString": "Apple Inc." }},
        {{ "key": "sector", "valueString": "Technology" }},
        {{ "key": "currentPrice", "valueNumber": 175.50 }},
        {{ "key": "recommendation", "valueString": "BUY" }},
        {{ "key": "targetPrice", "valueNumber": 200.00 }}
      ] }}
    ]
  }} }}
]
---END DETAILED_CARD_EXAMPLE---
"""

