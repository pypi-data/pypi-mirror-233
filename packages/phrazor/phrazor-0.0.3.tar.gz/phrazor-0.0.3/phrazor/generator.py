from copy import deepcopy
from typing import Union

from phrazor.analysis.analysis import Analysis
import phrazor.engine as engine
from phrazor.engine.publish import Publish, get_model_data
from phrazor.exceptions import AnalysisValidationException
from phrazor.messages.driver import get_error_message, raise_validation_error
from phrazor.utils import get_csv_data
from phrazor.validators.column_validator import (
    validate_date_column, validate_dimension_column, validate_metric_column
)
from phrazor.validators.data_validator import validate_column_in_data, validate_data
from phrazor.validators.filter_validator import validate_filter, validate_filter_column, validate_filter_values


class Phrazor:
    """
        Phrazor is a Python library that converts your data into textual insights.
    """
    SUPPORTED_ANALYSIS = [
        "descriptor", "change", "compare_measure", "compare_dimension", "target", "budget", "trend", "forecast"
    ]

    SUPPORTED_PERIOD = [
        "day", "week", "month", "quarter", "year"
    ]

    SUPPORTED_AGGREGATION = [
        "sum", "avg", "min", "max", "count"
    ]

    def __init__(self, api_key: Union[str, None] = None, openai_key: Union[str, None] = None) -> None:
        """
        @var: date_column: String column name or {"name": "", "period": ""}
            (Default period will be Month if string is given)
            period values: day, week, month, quarter, year

        @var: metric_column: list of string or dict ({"name": "", "aggregation": ""})
            (Default aggregation will be Sum if string is given)
            aggregation values: sum, vvg, min, max, count

        @var: dimension_column: List or String column name

        @var: dme: (optional) dict with dme properties

        @var: data: {
            "Column Name 1": [list of column 1 values in data],
            "Column Name 2": [list of column 2 values in data],
            "Column Name 3": [list of column 3 values in data]
        }

        @var analysis: analysis name
            "descriptor", "change", "compare_dimension", "compare_measure", "target", "budget" or "trend"

        @var: filters: [
            column_type: text
            operators supported: "in" or "not in"
            {
                "operator": "in", "column_name": "Region", "data_type": "text",
                "values": "Asia" or ["Asia", "Australia and Oceania"]
            },

            column_type: numeric
            operators supported:
                "equals", "not equals", "greater than", "greater than equals", "less than", "less than equals",
                "in range", "not in range" - (values should list if integer values eg :- [10, 50])
            {
                "operator": "in range", "column_name": "Total Cost", "data_type": "numeric",
                "values": [10, 50] (2 values for range filters operator)
            },
            {
                "operator": "equals", "column_name": "Total Cost", "data_type": "numeric",
                "values": 10 or [10, 50, 200]
            }

            column_type: timestamp
            operators supported: "in", "not in" or "in range"
            {
                "operator": "in", "column_name": "Order Date", "data_type": "timestamp", "period": "Month"
                "values": "April-2023" or ["March-2023", "April-2023"]
            }
        ]
        """
        self.api_key = api_key
        self.openai_key = openai_key
        self.date_column: Union[dict, None] = None
        self.metric_column: Union[list, None] = None
        self.dimension_column: Union[list, None] = None
        self.dme: dict = {}
        self.data: dict = {}
        self.filters: list = []
        self.analysis: Union[str, None] = None
        self.analysis_class: Union[Analysis, None] = None

        # focus on variables
        self.dimension_focus = None
        self.period_focus = None

        # dimension focus on variables
        self.focus_on_value: Union[list, str, None] = None
        self.compare_value_1: Union[str, None] = None
        self.compare_value_2: Union[str, None] = None

    def set_data(self, dict_or_path: Union[dict, str], is_csv: bool = False) -> None:
        """
        Assign data to class data variable
        @param dict_or_path: string if is_csv else dict
        @param is_csv: bool
        @return: None
        """
        data = get_csv_data(dict_or_path) if is_csv else dict_or_path
        validate_data(data)
        self.data = deepcopy(data)

    def set_date_column(self, date_column: Union[dict, str]) -> None:
        """
        Validate and assign date column to the date_column class variable
        @param date_column: dict or string
        @return: None
        """
        self.date_column = validate_date_column(date_column)
        validate_column_in_data(self.data, date_column=self.date_column)

    def set_metric_column(self, metric_column: Union[list, dict, str]) -> None:
        """
        Validate and assign metric column to the metric_column class variable
        @param metric_column: list, dict or string
        @return: None
        """
        metric_column_final = validate_metric_column(metric_column)
        if metric_column_final:
            if self.metric_column is None:
                self.metric_column = []
            self.metric_column = metric_column_final
        validate_column_in_data(self.data, metric_column=self.metric_column)

    def set_dimension_column(self, dimension_column: Union[list, str]) -> None:
        """
        Validate and assign dimension column to the dimension_column class variable
        @param dimension_column: list or string
        @return: None
        """
        self.dimension_column = validate_dimension_column(dimension_column)
        validate_column_in_data(self.data, dimension_column=self.dimension_column)

    def set_column_meta(
            self, date_column: Union[dict, str] = None, metric_column: Union[list, dict, str] = None,
            dimension_column: Union[list, str] = None
    ) -> None:
        """
        Set all the columns meta which are passed in the function
        @param date_column: dict or string
        @param metric_column: list, dict or string.
        @param dimension_column: string
        @return: None
        """
        self.date_column, self.metric_column, self.dimension_column = None, None, None
        if date_column:
            self.set_date_column(date_column)
        if metric_column:
            self.set_metric_column(metric_column)
        if dimension_column:
            self.set_dimension_column(dimension_column)

    def set_dme_meta(
            self, hierarchies=None, correlations=None, first_month=None, report_consumer=None, competitors=None
    ) -> None:
        self.dme = {
            'hierarchies': hierarchies if hierarchies else self.dme.get('hierarchies', []),
            'correlations': correlations if correlations else self.dme.get('correlations', []),
            'first_month': first_month if first_month else self.dme.get('first_month', 'january'),
            'report_consumer': report_consumer if report_consumer else self.dme.get('report_consumer', {}),
            'competitors': competitors if competitors else self.dme.get('competitors', [])
        }

    def reset_filters(self):
        self.filters = None

    def set_filter_meta(self, _filter: Union[list, dict]) -> None:
        self.filters = validate_filter(_filter)
        validate_filter_values(self.filters)
        validate_filter_column(self.data, self.filters)

    def publish(self, model_name: str, model_path: str) -> None:
        """
        Function is used to publish given meta inputs into a model file with extension .phrzr
        which later can be used to generate insights on different data.
        @param model_name: Models Name
        @param model_path: Model Location
        @return: None
        """
        Publish(
            request_data=self.analysis_class.request_data,
            analysis=self.analysis, date_column=self.date_column, metric_column=self.metric_column,
            dimension_column=self.dimension_column, dimension_focus=self.dimension_focus,
            filters=self.filters, dme=self.dme, focus_on_value=self.focus_on_value,
            compare_value_1=self.compare_value_1, compare_value_2=self.compare_value_2
        ).publish(
            model_name=model_name, model_path=model_path
        )

    def load_model(self, model_name: str, model_path: str = '') -> None:
        """
        Loads models inputs from mode_file.phrzr and allow user to use those inputs on their data.
        @param model_name: Model Name (without extension)
        @param model_path: Model Location
        @return: None
        """
        validate_data(self.data)
        published_data = get_model_data(model_name=model_name, model_path=model_path)
        for meta_key, meta_data in published_data.items():
            setattr(self, meta_key, meta_data)
        self.set_analysis(
            analysis=self.analysis, focus_on_value=self.focus_on_value, compare_value_1=self.compare_value_1,
            compare_value_2=self.compare_value_2
        )

    def set_analysis(
            self, analysis: str, focus_on_value: Union[list, str] = None, compare_value_1: str = None,
            compare_value_2: str = None
    ) -> None:
        """
        Check for supported analysis and then validate all the inputs which are provided are enough for summarizing
        that analysis or not.
        @param analysis: string analysis name
        @param focus_on_value: string list of string containing dimension column values
        @param compare_value_1: string - used for dimension comparison analysis
        @param compare_value_2: string - used for dimension comparison analysis
        @return: None
        """
        self.set_dme_meta()
        self.focus_on_value, self.compare_value_1, self.compare_value_2 = (
            focus_on_value, compare_value_1, compare_value_2
        )
        self.analysis = analysis.lower()
        self.analysis_class = Analysis(
            data=self.data, date_column=self.date_column, metric_column=self.metric_column,
            dimension_column=self.dimension_column, dimension_focus=self.dimension_focus, analysis=self.analysis,
            filters=self.filters, dme=self.dme,
            focus_on_value=focus_on_value, compare_value_1=compare_value_1, compare_value_2=compare_value_2
        )
        self.analysis_class.validate()
        self.analysis_class.add_advance_options()

    def check_and_set_analysis(
            self, on: Union[list, str] = None, focus_on_value: Union[list, str] = None, compare_value_1: str = None,
            compare_value_2: str = None
    ) -> None:
        validate_filter_column(self.data, self.filters)
        validate_column_in_data(self.data, date_column=self.date_column)
        validate_column_in_data(self.data, metric_column=self.metric_column)
        validate_column_in_data(self.data, dimension_column=self.dimension_column)
        analysis = None
        if on is None or not isinstance(on, (list, str)):
            raise_validation_error(
                validation_error=get_error_message(
                    validation_error='', _type='type_error', parameter_name='topics', data_types='list or string'
                ),
                error_class=AnalysisValidationException
            )
        if isinstance(on, str):
            if not on:
                message = f"Value for 'on' cannot be empty, following are supported analysis type :- " \
                          f'{", ".join(self.SUPPORTED_ANALYSIS)}'
                raise_validation_error(validation_error=message + '\n', error_class=AnalysisValidationException)
            if on.lower() not in self.SUPPORTED_ANALYSIS:
                message = f'[{on}] is not supported. SUPPORTED ANALYSIS :- {", ".join(self.SUPPORTED_ANALYSIS)}'
                raise_validation_error(validation_error=message + '\n', error_class=AnalysisValidationException)
            analysis = on
        if isinstance(on, list):
            if not on:
                on = self.show_topics()
                if isinstance(on, list) and on:
                    on = [topic['name'] for topic in on]
                    message = (f"Value for 'on' cannot be empty. From your given inputs, these topics can be selected: "
                               f'{", ".join(on)}')
                else:
                    message = 'Topics cannot be empty'
                raise_validation_error(validation_error=message + '\n', error_class=AnalysisValidationException)

            analysis = engine.ENGINE_CLASS(
                request_data={
                    'all_insight_topics': on, 'dimension_count': len(self.dimension_column or []),
                    'measure_count': len(self.metric_column or []), 'date_count': 1 if self.date_column else 0,
                    'focus_on_count':
                        1 if focus_on_value else 0 + (1 if compare_value_1 else 0) + (1 if compare_value_2 else 0)
                }, analysis_type='validate_topics', api_key=self.api_key, openai_key=self.openai_key
            ).post()
            analysis = analysis['analysis']
        self.set_analysis(
            analysis, focus_on_value=focus_on_value, compare_value_1=compare_value_1, compare_value_2=compare_value_2
        )
        if isinstance(on, list):
            self.analysis_class.request_data['insight_topics'] = on

    def get_summary(
            self, on: Union[list, str], focus_on_value: Union[list, str] = None, compare_value_1: str = None,
            compare_value_2: str = None, personality: str = 'default', verbosity: str = 'low',
            custom_prompt: str = ''
    ) -> dict:
        self.check_and_set_analysis(
            on=on, focus_on_value=focus_on_value, compare_value_1=compare_value_1,
            compare_value_2=compare_value_2
        )
        request_data = {
            **self.analysis_class.request_data,
            **{'personality': personality, 'verbosity': verbosity, 'custom_prompt': custom_prompt}
        }
        return engine.ENGINE_CLASS(
            request_data=request_data, analysis_type='summary', api_key=self.api_key, openai_key=self.openai_key
        ).post()

    def show_topics(self) -> dict:
        return engine.ENGINE_CLASS(
            request_data={
                'dimension': self.dimension_column or [], 'measure': self.metric_column, 'date': self.date_column,
                'period': self.date_column.get('period') if self.date_column else None
            },
            analysis_type='insight_topics', api_key=self.api_key, openai_key=self.openai_key
        ).post()

    def get_insights(
            self, on: Union[list, str], focus_on_value: Union[list, str] = None, compare_value_1: str = None,
            compare_value_2: str = None, formatted_sentence: bool = False, forecast_meta: dict = None,
    ) -> dict:
        self.check_and_set_analysis(
            on=on, focus_on_value=focus_on_value, compare_value_1=compare_value_1,
            compare_value_2=compare_value_2
        )
        self.analysis_class.request_data['formatted_sentence'] = formatted_sentence
        if forecast_meta:
            self.analysis_class.request_data['forecast_meta'] = forecast_meta
        if self.analysis == 'forecast':
            return engine.ENGINE_CLASS(
                request_data=self.analysis_class.request_data, analysis_type='forecast', api_key=self.api_key,
                openai_key=self.openai_key
            ).post()
        else:
            return engine.ENGINE_CLASS(
                request_data=self.analysis_class.request_data, analysis_type='insights', api_key=self.api_key,
                openai_key=self.openai_key
            ).post()
