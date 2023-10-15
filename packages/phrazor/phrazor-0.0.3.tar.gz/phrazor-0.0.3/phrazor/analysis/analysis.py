from copy import deepcopy

from phrazor.analysis_json.budget_json import get_budget
from phrazor.analysis_json.change_json import get_change
from phrazor.analysis_json.compare_json import get_dimension_compare, get_measure_compare
from phrazor.analysis_json.descriptor_json import get_descriptor
from phrazor.analysis_json.forecasting_json import get_forecast
from phrazor.analysis_json.target_json import get_target
from phrazor.analysis_json.trend_json import get_trend
from phrazor.exceptions import AnalysisValidationException
from phrazor.messages.driver import (
    get_error_message, raise_validation_error
)


class Analysis:
    def __init__(
            self, data, date_column, metric_column, dimension_column, dimension_focus, analysis, filters, dme,
            focus_on_value=None, compare_value_1=None, compare_value_2=None
    ):
        self.data = data
        self.date_column = date_column
        self.metric_column = metric_column
        self.dimension_column = dimension_column
        self.dimension_focus = dimension_focus
        self.analysis = analysis
        self.focus_on_values = self.set_focus_on(focus_on_value, compare_value_1, compare_value_2)
        self.filters = filters
        self.request_data = {}
        self.dme = dme

    def set_focus_on(self, focus_on_value, compare_value_1, compare_value_2):
        final_focus_on_values = None
        if self.analysis == 'compare_dimension':
            if (compare_value_1 and not compare_value_2) or (not compare_value_1 and compare_value_2):
                raise_validation_error(
                    validation_error=get_error_message(validation_error='', _type='compare_values'),
                    error_class=AnalysisValidationException
                )
            elif focus_on_value:
                raise_validation_error(
                    validation_error=get_error_message(validation_error='', _type='compare_values'),
                    error_class=AnalysisValidationException
                )
            else:
                if not isinstance(compare_value_1, str) or not isinstance(compare_value_2, str):
                    raise_validation_error(
                        validation_error=get_error_message(validation_error='', _type='compare_values_type'),
                        error_class=AnalysisValidationException
                    )
                final_focus_on_values = [[compare_value_1], [compare_value_2]]
        elif focus_on_value:
            if not isinstance(focus_on_value, (str, list)):
                raise_validation_error(
                    validation_error=get_error_message(
                        validation_error='', _type='type_error', parameter_name='focus_on_values',
                        data_types='string or list'
                    ),
                    error_class=AnalysisValidationException
                )
            final_focus_on_values = [[focus_on_value]] if isinstance(focus_on_value, str) else [focus_on_value]
        return final_focus_on_values

    def get_analysis_json(self):
        analysis_json_mapping = {
            'descriptor': get_descriptor,
            'change': get_change,
            'compare_measure': get_measure_compare,
            'compare_dimension': get_dimension_compare,
            'budget': get_budget,
            'target': get_target,
            'trend': get_trend,
            'forecast': get_forecast,
        }
        return analysis_json_mapping[self.analysis]()

    def get_input_count(self, input_type):
        input_count = {
            'measure': len(self.metric_column) if self.metric_column else 0,
            'dimension': len(self.dimension_column) if self.dimension_column else 0,
            'date': len([self.date_column]) if self.date_column else 0
        }
        try:
            return input_count[input_type]
        except KeyError:
            return 0

    def validate(self):
        validation_error = ''
        input_mapping = {
            'measure': self.metric_column,
            'dimension': self.dimension_column if self.dimension_column else [],
            'date': [self.date_column]
        }
        for _input in self.get_analysis_json()['inputs']:
            if not _input.get('advance'):
                if self.get_input_count(_input['name']) and _input['min'] <= self.get_input_count(_input['name']):
                    # updating input object for measure
                    if _input['name'] in ['measure', 'dimension']:
                        if _input['max'] < self.get_input_count(_input['name']):
                            validation_error = get_error_message(
                                validation_error=validation_error, _type='analysis_max_input_count',
                                max_input=_input['max'], input_name=_input['name'], analysis_name=self.analysis
                            )
                        self.request_data[_input['name']] = [input_mapping[_input['name']][0]]
                        if _input['max'] > 1 and self.get_input_count(_input['name']) > 1:
                            for _index in range(1, _input['max']):
                                if len(input_mapping[_input['name']]) - 1 >= _index:
                                    self.request_data[_input['name']].append(input_mapping[_input['name']][_index])
                    else:
                        self.request_data[_input['name']] = input_mapping[_input['name']][0]

                    # updating date column period
                    if _input['name'] == 'date':
                        self.request_data['period'] = input_mapping[_input['name']][0]['period']

                    # updating focus on values here
                    if _input['name'] == 'dimension' and _input['nested']:
                        focus_on_values = deepcopy(list(set(self.data[self.request_data[_input['name']][0]['name']])))
                        focus_on_values.insert(0, 'All')
                        focus_on_count = 0
                        focus_on_not_found = False
                        for nested_option in _input['nested']:
                            try:
                                if 'min' in nested_option and nested_option['min'] == 0:
                                    default_focus_on = self.focus_on_values[focus_on_count] \
                                        if self.focus_on_values else [focus_on_values[focus_on_count]]
                                else:
                                    focus_on_count += 1
                                    default_focus_on = self.focus_on_values[focus_on_count - 1] \
                                        if self.focus_on_values else [focus_on_values[focus_on_count]]
                                self.request_data[nested_option['name']] = {
                                    'label': ''.join(default_focus_on),
                                    'say_as': {'singular': '', 'plural': ''},
                                    'type': 'column',
                                    'value': default_focus_on
                                }
                            except IndexError:
                                focus_on_not_found = True
                        if focus_on_not_found:
                            validation_error = get_error_message(
                                validation_error=validation_error, _type='focus_on_count',
                                focus_on_count=focus_on_count, analysis_name=self.analysis
                            )
                else:
                    if _input.get('min', 0) > 0:
                        validation_error = get_error_message(
                            validation_error=validation_error, _type='analysis_input_count', min_input=_input['min'],
                            input_name=_input['name'], analysis_name=self.analysis
                        )

        if validation_error:
            raise_validation_error(validation_error=validation_error, error_class=AnalysisValidationException)

    def add_advance_options(self):
        self.request_data['data'] = self.data
        self.request_data['one_liner_function'] = self.get_analysis_json()['name']
        self.request_data['analysis'] = self.analysis
        self.request_data['filters'] = self.filters
        self.request_data['dme'] = self.dme
