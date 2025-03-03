from validators.factory import ValidatorFactory
from utils.yaml_loader import load_test_definitions

class NVaaSApp:
    def __init__(self):
        self.test_definitions = load_test_definitions()
        self.validator_factory = ValidatorFactory()

    def run_validation(self, current_state, previous_state=None):
        results = []
        for test_def in self.test_definitions:
            validator = self.validator_factory.get_validator(test_def["type"])
            result = validator.validate(
                test_def, 
                current_state=current_state, 
                previous_state=previous_state
            )
            results.append(result)
        return results
