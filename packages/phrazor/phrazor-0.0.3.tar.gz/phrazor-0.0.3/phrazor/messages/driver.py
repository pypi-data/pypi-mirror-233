from phrazor.messages.error_messages import (
    ANALYSIS_INPUT_COUNT_ERROR, ANALYSIS_MAX_INPUT_COUNT_ERROR, COLUMN_NOT_IN_DATA, COMPARE_VALUES_ERROR,
    COMPARE_VALUES_TYPE_ERROR, DATA_FIRST,
    EMPTY_DATA,
    EMPTY_PARAM, FILE_READ_ERROR, FILE_SAVE_ERROR, FILTER_COLUMN_NOT_IN_DATA,
    FILTER_VALUES_KEY_TYPE_ERROR,
    FILTER_VALUES_TYPE_ERROR,
    FOCUS_ON_COUNT_ERROR, KEY_ERROR, LIST_TYPE_ERROR, OPENAI_KEY_ERROR, SET_ANALYSIS_ERROR,
    TYPE_ERROR
)


def get_error_message(validation_error, _type, **kwargs):
    error_message_mapper = {
        'key_error': KEY_ERROR,
        'empty_param': EMPTY_PARAM,
        'openai_key_error': OPENAI_KEY_ERROR,
        'type_error': TYPE_ERROR,
        'list_type_error': LIST_TYPE_ERROR,
        'empty_data': EMPTY_DATA,
        'data_first': DATA_FIRST,
        'column_not_in_data': COLUMN_NOT_IN_DATA,
        'filter_column_not_in_data': FILTER_COLUMN_NOT_IN_DATA,
        'filter_values_type_error': FILTER_VALUES_TYPE_ERROR,
        'filter_values_key_type_error': FILTER_VALUES_KEY_TYPE_ERROR,
        'focus_on_count': FOCUS_ON_COUNT_ERROR,
        'analysis_input_count': ANALYSIS_INPUT_COUNT_ERROR,
        'analysis_max_input_count': ANALYSIS_MAX_INPUT_COUNT_ERROR,
        'compare_values': COMPARE_VALUES_ERROR,
        'compare_values_type': COMPARE_VALUES_TYPE_ERROR,
        'set_analysis_error': SET_ANALYSIS_ERROR,
        'file_save_error': FILE_SAVE_ERROR,
        'file_read_error': FILE_READ_ERROR
    }
    if not validation_error.startswith(get_start_validation_error()):
        validation_error += get_start_validation_error()
    return validation_error + error_message_mapper[_type].format(**kwargs)


def raise_validation_error(validation_error, error_class):
    if not validation_error.startswith(get_start_validation_error()):
        validation_error = get_start_validation_error() + validation_error
    if not validation_error.endswith(get_end_validation_error()):
        validation_error = validation_error + get_end_validation_error()
    raise error_class(message=validation_error)


def get_start_validation_error():
    return '\n---------->\n'


def get_end_validation_error():
    return '---------->'
