from phrazor.exceptions import AnalysisValidationException
from phrazor.messages.driver import get_error_message, raise_validation_error


def validate_request_data(request_data, task_type):
    if not request_data:
        raise_validation_error(
            validation_error=get_error_message(validation_error='', _type='set_analysis_error',
                                               task_type=task_type),
            error_class=AnalysisValidationException
        )
