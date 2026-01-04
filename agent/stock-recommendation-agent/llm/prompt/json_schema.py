STOCK_INVESTMENT_RECOMMENDATIONS_SCHEMA = r'''
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Stock Investment Recommendations",
  "description": "Description of the stock investment recommendations data.",
  "type": "object",
  "footer": {
      "type": "string",
      "description": "Texto de rodapé/observações gerais (fora do array).",
      "minLength": 1
   },
  "properties": {
    "data": {
      "type": "array",
      "description": "Descrição do array",
      "minItems": 0,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "properties": {
          "symbol": {
            "type": "string",
            "description": "Ticker/símbolo do ativo (ex.: GOOGL)."
          },
          "company": {
            "type": "string",
            "description": "Nome da empresa."
          },
          "sector": {
            "type": "string",
            "description": "Setor da empresa (ex.: Technology)."
          },
          "currentPrice": {
            "type": "number",
            "description": "Preço atual do ativo."
          },
          "recommendation": {
            "type": "string",
            "description": "Recomendação para o ativo.",
            "enum": ["BUY", "HOLD", "SELL"]
          },
          "targetPrice": {
            "type": "number",
            "description": "Preço alvo (target) do ativo."
          }
        },
        "required": ["symbol", "company", "sector", "currentPrice", "recommendation", "targetPrice"]
      }
    }
  },
  "required": ["data", "footer"]
}
'''