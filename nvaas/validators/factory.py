from .static import StaticValidator
from .diff import DiffValidator

class ValidatorFactory:
    def __init__(self):
        # Dictionary mapping test types to their respective validator classes
        self._validators = {
            "static": StaticValidator,
            "diff": DiffValidator
        }

    def get_validator(self, validator_type: str):
        """
        Creates and returns the appropriate validator based on the test type.
        
        Args:
            validator_type (str): The type of validator to create (e.g., "static" or "diff")
            
        Returns:
            BaseValidator: An instance of the appropriate validator
            
        Raises:
            ValueError: If the validator_type is not recognized
        """
        validator_class = self._validators.get(validator_type)
        if not validator_class:
            raise ValueError(f"Unknown validator type: {validator_type}")
        return validator_class()
