class ValidationException(Exception):
    # Parent of all Exception in data
    def __init__(self, message, params=None):
        self.message = message
        self.params = params

    # This very important in parent Exception
    def __str__(self):
        return self.message


class DataValidationException(ValidationException):
    pass


class ColumnValidationException(ValidationException):
    pass


class SummaryValidationException(ValidationException):
    pass


class FilterValidationException(ValidationException):
    pass


class AnalysisValidationException(ValidationException):
    pass


class PhrazorServerException(ValidationException):
    pass
