KEY_ERROR = '["{dict_key}"] should be present in the given {container} input dict\n'

OPENAI_KEY_ERROR = 'OpenAI Key should be provided to generate Summary.\n'

TYPE_ERROR = '[{parameter_name}] parameter can only be of type ({data_types})\n'

LIST_TYPE_ERROR = '[{parameter_name}] parameter list elements can only be of type ({data_types})\n'

EMPTY_DATA = 'Data you have provided is empty.\n'

EMPTY_PARAM = '{parameter_name} you have provided is empty.\n'

DATA_FIRST = 'Please set data before setting column meta or filter meta.\n'

COLUMN_NOT_IN_DATA = '[{column_name}] not found in data\n'

FILTER_COLUMN_NOT_IN_DATA = (
    'Filter column {column_name} is not present in data, please set filter meta again with filter column present '
    'in data or you can use reset_filters method to reset filters\n'
)

FILTER_VALUES_TYPE_ERROR = 'All filters values should contain only string or int type.\n'
FILTER_VALUES_KEY_TYPE_ERROR = 'Filter values key can only be of type string, dict or int.\n'

# Analysis Error Messages
FOCUS_ON_COUNT_ERROR = (
    "There should be {focus_on_count} focus on for {analysis_name} analysis\n"
    "If no focus on is passed then check if data has at least {focus_on_count} values\n"
)

ANALYSIS_INPUT_COUNT_ERROR = "There should be at least {min_input} {input_name} for {analysis_name} analysis\n"
ANALYSIS_MAX_INPUT_COUNT_ERROR = "There should be maximum {max_input} {input_name} for {analysis_name} analysis\n"

# Compare Dimension Error Messages
COMPARE_VALUES_ERROR = (
    'compare_value_1 and compare_value_2 both parameters is required for compare_dimension analysis\n'
)
COMPARE_VALUES_TYPE_ERROR = 'compare_value_1, compare_value_2 parameter should only be of type string\n'

SET_ANALYSIS_ERROR = (
    'You cannot {task_type} before setting analysis name, '
    'please call set_analysis function in order to set analysis.\n'
)

FILE_SAVE_ERROR = "Error saving the file '{model_path}': {exception_message}\n"

FILE_READ_ERROR = "Error reading the file '{model_path}': {exception_message}\n"
