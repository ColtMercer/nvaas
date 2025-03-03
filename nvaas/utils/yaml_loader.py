import yaml
import os
from pathlib import Path

def load_test_definitions(config_path=None):
    """
    Load test definitions from YAML configuration files.
    
    Args:
        config_path (str, optional): Path to the YAML config file or directory.
            If not provided, defaults to 'sample_tests' in the project root.
            
    Returns:
        list: List of test definition dictionaries
    """
    if config_path is None:
        # Default to sample_tests directory relative to this file
        config_path = Path(__file__).parent.parent / 'sample_tests'

    test_definitions = []
    
    if os.path.isfile(config_path):
        # Load single file
        with open(config_path, 'r') as f:
            # Use yaml.safe_load_all to handle multiple documents in one file
            docs = list(yaml.safe_load_all(f))
            # Filter out None values (empty documents)
            test_definitions.extend([doc for doc in docs if doc])
    elif os.path.isdir(config_path):
        # Load all .yml and .yaml files in directory
        for filename in os.listdir(config_path):
            if filename.endswith(('.yml', '.yaml')):
                file_path = os.path.join(config_path, filename)
                with open(file_path, 'r') as f:
                    docs = list(yaml.safe_load_all(f))
                    test_definitions.extend([doc for doc in docs if doc])
    else:
        raise FileNotFoundError(f"Config path not found: {config_path}")

    # Validate that each test definition has required fields
    for test in test_definitions:
        if not all(key in test for key in ["name", "description", "type", "commands"]):
            raise ValueError(f"Invalid test definition, missing required fields: {test}")

    return test_definitions
