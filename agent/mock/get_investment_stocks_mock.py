"""
Simple utility to read and return investment stocks JSON data as string.
"""
from pathlib import Path

def get_investment_stocks() -> str:
    """
    Reads investment_stocks_data.json and returns raw file content as string.
    
    Returns:
        Raw JSON file content as string
    """
    current_dir = Path(__file__).parent
    
    json_file = current_dir / "investment_stocks_data.json"
    
    with open(json_file, 'r', encoding='utf-8') as f:
        return f.read()
