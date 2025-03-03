from abc import ABC, abstractmethod
from typing import Dict, Optional

class BaseValidator(ABC):
    """
    Abstract base class for all validators.
    Defines the interface that all validator types must implement.
    """
    
    @abstractmethod
    def validate(self, 
                test_def: Dict, 
                current_state: Dict, 
                previous_state: Optional[Dict] = None) -> Dict:
        """
        Validate the test definition against the provided state.

        Args:
            test_def: Dictionary containing the test definition
            current_state: Current state of the system
            previous_state: Previous state (optional, used for diff tests)

        Returns:
            Dict containing validation results with at least:
            {
                "name": str,
                "description": str,
                "passed": bool,
                "details": str
            }
        """
        pass

    def _extract_command_params(self, commands: list) -> Dict:
        """
        Helper method to extract parameters from commands list.
        
        Args:
            commands: List of command dictionaries from test definition
            
        Returns:
            Dictionary of extracted parameters
        """
        params = {}
        for cmd in commands:
            for key, value in cmd.items():
                params[key] = value
        return params
