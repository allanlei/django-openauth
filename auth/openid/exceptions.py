from django.core.exceptions import ValidationError

class OpenIDValidationError(ValidationError):
    pass
