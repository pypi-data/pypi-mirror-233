import base64
import json
import os

from phrazor.engine.exceptions import FileReadException, FileSaveException
from phrazor.messages.driver import get_error_message, raise_validation_error
from phrazor.validators.request_data_validator import validate_request_data


class Publish:
    MODEL_EXTENSION = '.d2i'

    def __init__(self, request_data=None, **kwargs):
        self.request_data = request_data
        self.publish_data = kwargs
        validate_request_data(request_data, 'publish_data')

    def publish(self, model_name, model_path=''):
        encoded_json = encode_to_base64(json.dumps(self.publish_data))
        save_to_file(
            model_path=os.path.join(model_path, model_name + self.MODEL_EXTENSION),
            content=encoded_json
        )


def get_model_data(model_name, model_path=''):
    encoded_content = read_from_file(model_path=os.path.join(model_path, model_name + Publish.MODEL_EXTENSION))
    decoded_string = decode_from_base64(encoded_string=encoded_content)
    return json.loads(decoded_string)


# Function to encode a string to base64
def encode_to_base64(input_string):
    encoded_bytes = base64.b64encode(input_string.encode())
    return encoded_bytes.decode()


# Function to save a string to a file
def save_to_file(model_path, content):
    try:
        with open(model_path, "w") as file:
            file.write(content)
            file.close()
    except IOError as e:
        raise_validation_error(
            validation_error=get_error_message(
                validation_error='', _type='file_save_error', model_path=model_path, exception_message=str(e)
            ),
            error_class=FileSaveException
        )


# Function to read a string from a file
def read_from_file(model_path):
    try:
        with open(model_path, "r") as file:
            file_content = file.read()
            file.close()
        return file_content
    except IOError as e:
        raise_validation_error(
            validation_error=get_error_message(
                validation_error='', _type='file_read_error', model_path=model_path, exception_message=str(e)
            ),
            error_class=FileReadException
        )


# Function to decode a base64-encoded string
def decode_from_base64(encoded_string):
    decoded_bytes = base64.b64decode(encoded_string)
    return decoded_bytes.decode()
