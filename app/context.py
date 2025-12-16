import json
import os
from typing import Dict, Any

def load_business_profile() -> Dict[str, Any]:
    """
    Loads the business context from the static JSON file.
    
    Returns:
        Dict[str, Any]: The business profile data.
    
    Raises:
        FileNotFoundError: If the profile file does not exist.
        json.JSONDecodeError: If the file content is invalid JSON.
    """
    # Determine the absolute path to the data file
    # Assuming the app is run from the project root or similar structure
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "business_profile.json")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Business profile not found at {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return data
