"""
Simple utility to read and return JSON data as string.
"""

import json
import os
from pathlib import Path


def get_restaurant_data_as_string() -> str:
    """
    Reads restaurant_data.json and returns it as a formatted string.
    
    Returns:
        JSON content as a formatted string
    """
    # Get the directory where this file is located
    current_dir = Path(__file__).parent
    
    # Path to the JSON file
    json_file = current_dir / "restaurant_data.json"
    
    # Read and return JSON as string
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        return json.dumps(json_data, indent=2, ensure_ascii=False)


def get_restaurant_data_raw() -> str:
    """
    Reads restaurant_data.json and returns raw file content as string.
    
    Returns:
        Raw JSON file content as string
    """
    # Get the directory where this file is located
    current_dir = Path(__file__).parent
    
    # Path to the JSON file
    json_file = current_dir / "restaurant_data.json"
    
    # Read and return raw content
    with open(json_file, 'r', encoding='utf-8') as f:
        return f.read()
