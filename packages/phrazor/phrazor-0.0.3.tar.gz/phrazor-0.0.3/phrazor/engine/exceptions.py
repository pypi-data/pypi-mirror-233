class PublishException(Exception):
    # Parent of all Exception in data
    def __init__(self, message, params=None):
        self.message = message
        self.params = params

    # This very important in parent Exception
    def __str__(self):
        return self.message


class PublishValidationException(PublishException):
    pass


class FileSaveException(PublishException):
    pass


class FileReadException(PublishException):
    pass
