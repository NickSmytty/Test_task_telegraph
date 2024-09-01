import allure
import pytest
import jsonschema
from config import SCHEMA
from jsonschema import validate
from common.allure_attach import attach


class BasePost:
    def __init__(self):
        self.response = None
        self.response_json = None
        self.get_response = None
        self.errors = []
        self.xfails = []

    def check_status_code(self, code: int) -> None:
        """
        Checks response status code.
        """
        with allure.step(f"Check status code equal to {code}"):
            if self.response.status_code != code:
                pytest.fail(
                    f"Status code must be {code}, not {self.response.status_code}."
                )

    def validate_response(self) -> None:
        """
        Defines one or more requests and validate response by schema in config.py
        """
        if isinstance(self.response_json, list):
            with allure.step("Validate all posts"):
                for post in self.response_json:
                    self._validate_single_response(post, SCHEMA)
        else:
            with allure.step("Validate single post"):
                self._validate_single_response(self.response_json, SCHEMA)

    def _validate_single_response(self, instance: dict, schema: dict):
        """
        Validate response by schema in config.py
        """
        try:
            validate(instance=instance, schema=schema)

        except jsonschema.exceptions.ValidationError as e:
            self.errors.append(f"Validation error: {str(e)}")

    def check_results(self):
        """
        Checks fails and xfails in the end of test
        """
        if self.errors or self.xfails:
            if self.xfails:
                formatted_xfail = "\n".join(self.xfails)
                attach("Expected Failures", formatted_xfail)

            if self.errors:
                formatted_errors = "\n".join(self.errors)
                attach("Failures", formatted_errors)

            if self.errors and self.xfails:
                pytest.fail(
                    f"Test failed with {len(self.errors)} errors and {len(self.xfails)} expected failures."
                )

            elif self.errors:
                pytest.fail(f"Test failed with {len(self.errors)} errors")

            elif self.xfails:
                pytest.xfail(f"Test xfailed with {len(self.xfails)} expected failures")
