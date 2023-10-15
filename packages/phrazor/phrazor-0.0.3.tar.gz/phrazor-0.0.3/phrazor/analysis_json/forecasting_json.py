from copy import deepcopy

from phrazor.analysis_json.analysis_base_json import (
    get_base_date, get_base_dimension, get_base_measure,
    get_focus_on_sections
)


def get_forecast_date():
    forecast_date = deepcopy(get_base_date())
    forecast_date.update(
        {
            "mandatory_inputs": True,
            "rules": {
                "0": [{"input": "measure", "properties": {"min": 1, "max": 1}},
                      {"input": "dimension", "properties": {"min": 0, "max": 1}}],
                "1": [{"input": "measure", "properties": {"min": 1, "max": 1}},
                      {"input": "dimension", "advanced": [
                          {"inputs": [{"name": "measure", "selected": 1}], "properties": {"min": 0, "max": 1}}
                      ]}]
            }
        }
    )
    return forecast_date


def get_forecast_measure():
    forecast_measure = deepcopy(get_base_measure())
    forecast_measure.update(
        {
            "max": 3,
            "rules": {
                "0": [{"input": "date", "properties": {"min": 1, "max": 1}},
                      {"input": "dimension", "properties": {"min": 0, "max": 1}}],
                "1": [{"input": "date", "properties": {"min": 1, "max": 1}},
                      {"input": "dimension", "properties": {"min": 0, "max": 1}},
                      {"input": "focus_on", "advanced": [
                          {"inputs": [{"name": "dimension", "selected": 1}], "properties": {"min": 1, "max": 1}},
                          {"inputs": [{"name": "dimension", "selected": 0}], "properties": {"min": 0, "max": 1}}
                      ]}]
            }
        }
    )
    return forecast_measure


def get_forecast_dimension():
    forecast_dimension = deepcopy(get_base_dimension())
    forecast_dimension.update(
        {
            "max": 1,
            "rules": {
                "0": [
                    {"input": "date", "properties": {"min": 1, "max": 1}},
                    {"input": "measure", "properties": {"min": 1, "max": 1}},
                    {"input": "focus_on", "properties": {"min": 0, "max": 1}}
                ],
                "1": [
                    {"input": "date", "properties": {"min": 1, "max": 1}},
                    {"input": "measure", "properties": {"min": 1, "max": 1}},
                    {"input": "focus_on", "properties": {"min": 1, "max": 1}}
                ]
            },
            "nested": [
                {
                    "name": "focus_on",
                    "supported_types": [
                        "text", "variable"
                    ],
                    "max": 1,
                    "rules": {
                        "0": [{"input": "date", "properties": {"min": 1, "max": 1}},
                              {"input": "measure", "properties": {"min": 1, "max": 1}},
                              ],
                        "1": [{"input": "date", "properties": {"min": 1, "max": 1}},
                              {"input": "measure", "properties": {"min": 1, "max": 1}}]
                    },
                    "get_values": True,
                    "label": "Focus On",
                    "min": 1,
                    "description": "",
                    "spread": True,
                    "sections": [get_focus_on_sections()['variable'], get_focus_on_sections()['column']]
                }
            ],
        }
    )
    return forecast_dimension


def get_forecast():
    return {
        "name": "forecast",
        "label": "Forecast",
        "description": "",
        "inputs": [
            get_forecast_date(),
            get_forecast_measure(),
            get_forecast_dimension()
        ]
    }
