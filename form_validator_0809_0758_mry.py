# 代码生成时间: 2025-08-09 07:58:00
import starlette.requests
from pydantic import BaseModel, EmailStr, ValidationError, validator
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


class FormValidationError(Exception):
    """ Custom exception for form validation errors. """
    def __init__(self, errors):
        super().__init__(errors)
        self.errors = errors



class FormValidator(BaseModel):
    """ Pydantic model to validate form data. """
    name: str
    email: EmailStr
    age: int

    # Custom validators
    @validator("name")
    def name_must_be_not_empty(cls, v):
        if not v:
            raise ValueError("Name cannot be empty")
        return v

    @validator("age")
    def check_age(cls, v):
        if not (0 < v < 150):
            raise ValueError("Age must be between 1 and 149")
        return v

    # Method to validate form data
    def validate(self, data: dict):
        """ Validate form data using Pydantic model. """
        try:
            return self.parse_obj(data)
        except ValidationError as e:
            # Raise custom exception with validation errors
            raise FormValidationError(
                {
                    "message": "Form validation failed",
                    "errors": e.errors(),
                }
            )


# Example usage:
# form_data = {
#     "name": "John",
#     "email": "john@example.com",
#     "age": 30,
# }
#
# validator = FormValidator()
# try:
#     valid_data = validator.validate(form_data)
#     print("Valid data:", valid_data)
# except FormValidationError as e:
#     print("Validation errors: