from phrazor.exceptions import FilterValidationException
from phrazor.messages.driver import get_error_message, raise_validation_error


def validate_filter(_filter):
    """
    Validate filter format and keys which are required inside filter dict
    @param _filter: list or dict
    @return: Filters list
    """
    final_filter = []
    validation_error = ''
    if isinstance(_filter, dict):
        required_keys = ['operator', 'column_name', 'values', 'data_type']
        for key in required_keys:
            if key not in _filter:
                validation_error = get_error_message(
                    validation_error=validation_error, _type='key_error', dict_key=key, container='filter'
                )
        final_filter.append(_filter)
    elif isinstance(_filter, list):
        for _filter_dict in _filter:
            final_filter.extend(validate_filter(_filter_dict))
    else:
        validation_error = get_error_message(
            validation_error=validation_error, _type='type_error', parameter_name='filter',
            data_types='list or dict'
        )
    if validation_error:
        raise_validation_error(validation_error=validation_error, error_class=FilterValidationException)

    return final_filter


def validate_filter_values(filters):
    """
    Validate the values inside each filter dict should be of correct format which is (string or list)
    @param filters: list
    @return: None
    """
    for _filter in filters:
        if isinstance(_filter['values'], str):
            _filter['values'] = [str(_filter['values'])]
        elif isinstance(_filter['values'], int):
            _filter['values'] = [_filter['values']]
        elif isinstance(_filter['values'], list):
            if not all(isinstance(value, (str, int)) for value in _filter['values']):
                validation_error = get_error_message(validation_error='', _type='filter_values_type_error')
                raise_validation_error(validation_error=validation_error, error_class=FilterValidationException)
            # converting all values to string to keep same format before sending it to the Data2Insight backend engine
            _filter['values'] = [value for value in _filter['values']]
        else:
            validation_error = get_error_message(validation_error='', _type='filter_values_key_type_error')
            raise_validation_error(validation_error=validation_error, error_class=FilterValidationException)


def validate_filter_column(data, filters):
    validation_error = ''
    for _filter in filters:
        if _filter['column_name'] not in data:
            validation_error = get_error_message(
                validation_error=validation_error, _type='filter_column_not_in_data', column_name=_filter["column_name"]
            )
    if validation_error:
        raise_validation_error(validation_error=validation_error, error_class=FilterValidationException)
