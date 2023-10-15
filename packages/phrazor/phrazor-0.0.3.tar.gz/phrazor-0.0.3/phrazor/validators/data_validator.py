from phrazor.exceptions import DataValidationException
from phrazor.messages.driver import (
    get_error_message, raise_validation_error
)


def validate_data(data):
    """
    Validate if data is empty or not.
    @param data: dict
    @return: None
    """
    if isinstance(data, dict):
        if not len(data.keys()):
            validation_error = get_error_message(validation_error='', _type='empty_data')
            raise_validation_error(validation_error=validation_error, error_class=DataValidationException)
        if not validate_columns_have_same_length(data):
            validation_error = (
                "Columns have different lengths. "
                "Please ensure that all columns have the same number of rows.\n"
            )
            raise_validation_error(validation_error=validation_error, error_class=DataValidationException)
        if not validate_number_of_cells(data):
            validation_error = (
                "Your data contains too many cells. "
                "Please limit the number of rows and columns to avoid exceeding 200,000 cells.\n"
            )
            raise_validation_error(validation_error=validation_error, error_class=DataValidationException)
    else:
        validation_error = get_error_message(
            validation_error='', _type='type_error', parameter_name='data', data_types='dictionary'
        )
        raise_validation_error(validation_error=validation_error, error_class=DataValidationException)


def validate_column_in_data(data, date_column=None, metric_column=None, dimension_column=None):
    """
    Checks if column meta columns are present in the data or not.
    @param data: dict
    @param date_column: dict
    @param metric_column: list
    @param dimension_column: list
    @return: None
    """
    if not data:
        validation_error = get_error_message(validation_error='', _type='data_first')
        raise_validation_error(validation_error=validation_error, error_class=DataValidationException)

    column_names = []
    if date_column is not None:
        column_names.append(date_column['name'])
    if metric_column is not None:
        column_names.extend([column['name'] for column in metric_column])
    if dimension_column is not None:
        column_names.extend([column['name'] for column in dimension_column])

    validation_error = ''
    for column_name in column_names:
        if column_name not in data:
            validation_error = get_error_message(
                validation_error=validation_error, _type='column_not_in_data', column_name=column_name
            )

    if validation_error:
        raise_validation_error(validation_error=validation_error, error_class=DataValidationException)


def validate_number_of_cells(data):
    num_cols = len(data.keys())
    num_rows = len(next(iter(data.values())))
    return (num_cols * num_rows) < 200000


def validate_columns_have_same_length(data):
    column_lengths = [len(values) for values in data.values()]

    if all(length == column_lengths[0] for length in column_lengths):
        return True
    else:
        return False
