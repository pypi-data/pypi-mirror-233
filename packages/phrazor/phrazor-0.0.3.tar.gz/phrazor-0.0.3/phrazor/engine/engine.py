from json import JSONDecodeError
from requests.exceptions import JSONDecodeError as RequestsJSONDecodeError

import requests
import phrazor
from phrazor.exceptions import PhrazorServerException, SummaryValidationException
from phrazor.messages.driver import get_error_message, raise_validation_error


class PhrazorEngine:
    def __init__(self, request_data, analysis_type, **kwargs):
        self.request_data = request_data
        self.analysis_type = analysis_type
        self.openai_key = kwargs.get('openai_key', phrazor.OPENAI_KEY) or phrazor.OPENAI_KEY
        self.api_key = kwargs.get('api_key', phrazor.API_KEY) or phrazor.API_KEY
        self.validate()

    def validate(self):
        if self.analysis_type == 'summary':
            if self.openai_key:
                self.request_data['openai_key'] = self.openai_key
            else:
                raise_validation_error(
                    validation_error=get_error_message(validation_error='', _type='openai_key_error'),
                    error_class=SummaryValidationException
                )

    @staticmethod
    def get_engine_url():
        from phrazor import CUSTOM_SERVER
        return CUSTOM_SERVER if CUSTOM_SERVER else 'https://platform.phrazor.ai'

    def get_analysis_url(self):
        url_mapper = {
            'insights': '/analysis/v1/insights/',
            'summary': '/summarise/',
            'insight_topics': '/analysis/v1/insight-topics/',
            'validate_topics': '/analysis/validate-topics/',
            'forecast': '/analysis/v1/forecast/',
        }
        return self.get_engine_url() + url_mapper[self.analysis_type]

    def post(self):
        try:
            response = requests.post(
                url=self.get_analysis_url(), json=self.request_data,
                headers={
                    'Authorization': f'AccessToken {self.api_key}'
                }
            )
        except requests.exceptions.ConnectionError as e:
            response = None

        try:
            if response is None:
                raise_validation_error(
                    validation_error='Could not connect to server, please try again later.' + '\n',
                    error_class=PhrazorServerException
                )
            elif response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise_validation_error(
                    validation_error=str(response.text) + '\n',
                    error_class=PhrazorServerException
                )
            else:
                raise_validation_error(
                    validation_error=str(response.json()) + '\n',
                    error_class=PhrazorServerException
                )
        except (JSONDecodeError, RequestsJSONDecodeError):
            if 'Server Error (500)' in response.text:
                raise_validation_error(
                    validation_error='Unable to connect with Phrazor SDK server, please try again after some time.'
                                     + '\n',
                    error_class=PhrazorServerException
                )
            else:
                raise_validation_error(
                    validation_error=response.text + '\n',
                    error_class=PhrazorServerException
                )
