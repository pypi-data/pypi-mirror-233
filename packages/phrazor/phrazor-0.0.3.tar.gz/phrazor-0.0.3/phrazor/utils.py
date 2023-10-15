import csv

from phrazor.engine.exceptions import FileReadException
from phrazor.messages.driver import get_error_message, raise_validation_error


def get_csv_data(csv_path):
    """
    Assign data from csv to class data variable
    @param csv_path: CSV file's path
    @return: data_dict
    """
    data = {}
    try:
        if not isinstance(csv_path, str):
            raise_validation_error(
                validation_error=get_error_message(
                    validation_error='', _type='type_error', parameter_name='dict_or_path', data_types='string'
                ),
                error_class=FileReadException
            )

        with open(csv_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                for column, value in row.items():
                    if column in data:
                        data[column].append(value)
                    else:
                        data[column] = [value]
        return data
    except IOError as e:
        raise_validation_error(
            validation_error=get_error_message(
                validation_error='', _type='file_read_error', model_path=csv_path, exception_message=str(e)
            ),
            error_class=FileReadException
        )
