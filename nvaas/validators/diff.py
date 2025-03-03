from typing import Dict, Optional
from jdiff import JsonDiffer
from .base import BaseValidator

class DiffValidator(BaseValidator):
    """
    Validator for diff tests that compare before and after states.
    """
    
    def __init__(self):
        self.differ = JsonDiffer()

    def validate(self, 
                test_def: Dict, 
                current_state: Dict, 
                previous_state: Optional[Dict] = None) -> Dict:
        """
        Validate a diff test comparing before and after states.
        """
        result = {
            "name": test_def["name"],
            "description": test_def["description"],
            "passed": False,
            "details": ""
        }

        if not previous_state:
            result["details"] = "Error: Previous state required for diff validation"
            return result

        try:
            params = self._extract_command_params(test_def["commands"])
            command = params["command"]
            key = params["key"]
            match_type = params["match_type"]
            tolerance = float(params["match_value"])

            # Extract values using jdiff
            before_value = self.differ.get_value(previous_state, f"{command}.{key}")
            after_value = self.differ.get_value(current_state, f"{command}.{key}")

            if before_value is not None and after_value is not None:
                if match_type == "tolerance_percent":
                    # Calculate percentage difference
                    before_float = float(before_value)
                    after_float = float(after_value)
                    if before_float != 0:  # Avoid division by zero
                        diff_percent = abs(after_float - before_float) / before_float * 100
                        result["passed"] = diff_percent <= tolerance
                        result["details"] = (
                            f"Before: {before_value}, After: {after_value}, "
                            f"Difference: {diff_percent:.2f}%, "
                            f"Tolerance: {tolerance}%"
                        )
                    else:
                        result["details"] = "Error: Cannot calculate percentage difference from zero"
            else:
                result["details"] = "Error: Could not extract values for comparison"

        except Exception as e:
            result["details"] = f"Error during validation: {str(e)}"

        return result
