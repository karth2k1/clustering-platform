"""JSON parsing utilities for handling various JSON structures"""
import json
import pandas as pd
from typing import Tuple, Optional, Dict, Any, List
from pathlib import Path


def detect_json_structure(json_data: Any) -> str:
    """Detect JSON structure type"""
    if isinstance(json_data, list):
        if len(json_data) > 0 and isinstance(json_data[0], dict):
            return "array_of_objects"
        return "array"
    elif isinstance(json_data, dict):
        # Check if it's nested objects
        if len(json_data) == 1 and isinstance(list(json_data.values())[0], list):
            return "nested_objects"
        return "object"
    return "unknown"


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """Flatten a nested dictionary"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # Handle lists: convert to string or extract if single element
            if len(v) == 0:
                items.append((new_key, None))
            elif len(v) == 1:
                if isinstance(v[0], dict):
                    items.extend(flatten_dict(v[0], new_key, sep=sep).items())
                else:
                    items.append((new_key, v[0]))
            else:
                # Multiple elements: join as string or create multiple columns
                items.append((new_key, ', '.join(str(x) for x in v)))
        else:
            items.append((new_key, v))
    return dict(items)


def parse_json_content(json_content: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """Parse JSON content and convert to DataFrame"""
    try:
        # Try parsing as JSON
        json_data = json.loads(json_content)
        
        # Detect structure
        structure_type = detect_json_structure(json_data)
        
        if structure_type == "array_of_objects":
            # Flatten each object
            flattened = [flatten_dict(obj) for obj in json_data]
            df = pd.DataFrame(flattened)
        elif structure_type == "nested_objects":
            # Handle nested structure
            flattened = flatten_dict(json_data)
            df = pd.DataFrame([flattened])
        elif structure_type == "object":
            # Single object
            flattened = flatten_dict(json_data)
            df = pd.DataFrame([flattened])
        else:
            df = pd.DataFrame(json_data)
        
        return df, None
        
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON format: {e}"
    except Exception as e:
        return None, f"Error parsing JSON: {e}"


def parse_json_file(file_path: Path) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """Parse JSON file and convert to DataFrame"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try JSON Lines format first
        if '\n' in content and content.strip().startswith('{'):
            lines = [line.strip() for line in content.strip().split('\n') if line.strip()]
            json_objects = []
            for line in lines:
                try:
                    json_objects.append(json.loads(line))
                except:
                    pass
            if json_objects:
                json_data = json_objects
            else:
                json_data = json.loads(content)
        else:
            json_data = json.loads(content)
        
        # Detect structure
        structure_type = detect_json_structure(json_data)
        
        if structure_type == "array_of_objects":
            flattened = [flatten_dict(obj) for obj in json_data]
            df = pd.DataFrame(flattened)
        elif structure_type == "nested_objects":
            flattened = flatten_dict(json_data)
            df = pd.DataFrame([flattened])
        elif structure_type == "object":
            flattened = flatten_dict(json_data)
            df = pd.DataFrame([flattened])
        else:
            df = pd.DataFrame(json_data)
        
        return df, None
        
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON format: {e}"
    except Exception as e:
        return None, f"Error parsing JSON file: {e}"


def extract_file_metadata(df: pd.DataFrame) -> Dict[str, Any]:
    """Extract metadata from DataFrame"""
    return {
        "shape": list(df.shape),
        "columns": df.columns.tolist(),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": df.isnull().sum().to_dict(),
        "memory_usage": int(df.memory_usage(deep=True).sum())
    }

