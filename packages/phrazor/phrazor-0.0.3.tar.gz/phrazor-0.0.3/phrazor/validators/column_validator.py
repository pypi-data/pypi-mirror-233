from phrazor.exceptions import ColumnValidationException
from phrazor.messages.driver import (
    get_error_message, raise_validation_error
)


def validate_date_column(date_column):
    """
    Validate date column input and converts it into the dict format.
    Raises proper exception if expected format is not given.
    @param date_column: String column name or {"name": "", "period": ""}
            (Default period will be Month if string is given)
    @return: dict {"name": "column name", "period": "month"}
    """
    from phrazor import Phrazor
    date_column_final = None
    validation_error = ''
    if not date_column:
        validation_error = get_error_message(
            validation_error=validation_error, _type='empty_param', parameter_name='date_column'
        )
    elif isinstance(date_column, str):
        date_column_final = {'name': date_column, 'period': 'Month'}
    elif isinstance(date_column, dict):
        if date_column.get('period') and date_column['period'].lower() not in Phrazor.SUPPORTED_PERIOD:
            raise_validation_error(
                validation_error=f"Invalid period type '{date_column['period']}'. Supported period types are: "
                                 f'{", ".join(Phrazor.SUPPORTED_PERIOD)}\n',
                error_class=ColumnValidationException)
        required_keys = ['name', 'period']
        for key in required_keys:
            if key not in date_column:
                validation_error = get_error_message(
                    validation_error=validation_error, _type='key_error', dict_key=key, container='date'
                )
        if not validation_error:
            date_column_final = date_column
    else:
        validation_error = get_error_message(
            validation_error=validation_error, _type='type_error', parameter_name='date_column',
            data_types='string or dictionary'
        )
    if validation_error:
        raise_validation_error(validation_error=validation_error, error_class=ColumnValidationException)
    return date_column_final


def validate_metric_column(metric_column):
    """
    Validate metric column input and converts it into the list format.
    Raises proper exception if expected format is not given.
    @param metric_column: list of string or dict ({"name": "", "aggregation": ""})
            (Default aggregation will be Sum if string is given)
    @return: list [{"name": "column name", "aggregation": "sum"}]
    """
    from phrazor import Phrazor
    metric_column_final = []
    validation_error = ''
    if isinstance(metric_column, str):
        metric_column_final.append({'name': metric_column, 'aggregation': 'Sum'})
    elif isinstance(metric_column, dict):
        if (
                metric_column.get('aggregation')
                and metric_column['aggregation'].lower() not in Phrazor.SUPPORTED_AGGREGATION
        ):
            raise_validation_error(
                validation_error=f"Invalid aggregation type '{metric_column['aggregation']}'. "
                                 f'Supported aggregation types are: {", ".join(Phrazor.SUPPORTED_AGGREGATION)}\n',
                error_class=ColumnValidationException)
        required_keys = ['name', 'aggregation']
        for key in required_keys:
            if key not in metric_column:
                validation_error = get_error_message(
                    validation_error=validation_error, _type='key_error', dict_key=key, container='metric'
                )
        if not validation_error:
            metric_column_final.append(metric_column)
    elif isinstance(metric_column, list):
        for metric in metric_column:
            metric_column_final.extend(validate_metric_column(metric))
    if validation_error:
        raise_validation_error(validation_error=validation_error, error_class=ColumnValidationException)
    return metric_column_final


def validate_dimension_column(dimension_column):
    """
    Validate dimension column input and converts it into the list format.
    Raises proper exception if expected format is not given.
    @param dimension_column: string column name or list of string
    @return: list
    """
    dimension_column_final = None
    validation_error = ''
    if isinstance(dimension_column, str):
        dimension_column_final = [{"name": dimension_column}]
    elif isinstance(dimension_column, list):
        if not all(isinstance(column, str) for column in dimension_column):
            validation_error = get_error_message(
                validation_error=validation_error, _type='list_type_error', parameter_name='dimension_column',
                data_types='string'
            )
        dimension_column_final = [{"name": column} for column in dimension_column]
    else:
        validation_error = get_error_message(
            validation_error=validation_error, _type='type_error', parameter_name='dimension_column',
            data_types='string or list'
        )
    if validation_error:
        raise_validation_error(validation_error=validation_error, error_class=ColumnValidationException)
    return dimension_column_final
