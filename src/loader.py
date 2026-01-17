import json
import os

import yaml

def load_openapi_spec(file_path):
    """
    Load an OpenAPI spec from a YAML or JSON file.

    Args:
        file_path (str): Path to the specification file.

    Returns:
        dict: The parsed specification as a dictionary, or None if loading fails.
    """
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.endswith(('.yaml', '.yml')):
                # Safe load for YAML
                spec = yaml.safe_load(f)
            else:
                # Default to JSON for other extensions or no extension
                spec = json.load(f)

        print(f"Successfully loaded {file_path}")
        return spec

    except (yaml.YAMLError, json.JSONDecodeError, IOError) as e:
        print(f"Error parsing {file_path}: {e}")
        return None
