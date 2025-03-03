from typing import Dict, Optional
from jdiff import JsonDiffer
from .base import BaseValidator

class StaticValidator(BaseValidator):
    """
    Validator for static tests that check current state against fixed values.
    """
    
    def __init__(self):
        self.differ = JsonDiffer()

    def validate(self, 
                test_def: Dict, 
                current_state: Dict, 
                previous_state: Optional[Dict] = None) -> Dict:
        """
        Validate a static test against current state.
        """
        result = {
            "name": test_def["name"],
            "description": test_def["description"],
            "passed": False,
            "details": ""
        }

        try:
            params = self._extract_command_params(test_def["commands"])
            command = params["command"]
            key = params["key"]
            match_type = params["match_type"]
            match_value = params["match_value"]

            # Extract actual value using jdiff
            actual_value = self.differ.get_value(current_state, f"{command}.{key}")

            # Perform validation based on match_type
            if match_type == "exact":
                result["passed"] = str(actual_value) == str(match_value)
            elif match_type == "max_value":
                result["passed"] = float(actual_value) <= float(match_value)
            elif match_type == "contains":
                result["passed"] = str(match_value) in str(actual_value)

            result["details"] = f"Expected: {match_value}, Actual: {actual_value}"

        except Exception as e:
            result["details"] = f"Error during validation: {str(e)}"

        return result
