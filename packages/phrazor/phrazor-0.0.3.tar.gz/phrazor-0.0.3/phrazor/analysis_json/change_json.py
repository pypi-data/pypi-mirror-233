from copy import deepcopy

from phrazor.analysis_json.analysis_base_json import (
    get_base_date, get_base_dimension, get_base_measure,
    get_base_period, get_base_qualifier, get_focus_on_sections
)


def get_change_period():
    change_period = deepcopy(get_base_period())
    change_period.update(
        {
            "options": [
                {
                    "label": "Last 2 Periods",
                    "value": {
                        "formula": "LatestPeriods(``date``,  ChangeCase(period,\"lower\"), 2, custom_start_period)",
                        "label": "Last 2 Periods",
                        "name": "last_2_period",
                    },
                }
            ]
        }
    )
    return change_period


def get_change_date():
    change_date = deepcopy(get_base_date())
    change_date.update(
        {
            "rules": {
                "0": [
                    {"input": "dimension", "properties": {"min": 1}},
                    {"input": "period_qualifier", "properties": {"max": 0}},
                    {"input": "focus_on", "properties": {"max": 1}}
                ],
                "1": [
                    {"input": "dimension", "properties": {"min": 0}},
                    {"input": "focus_on", "properties": {"max": 1}},
                    {"input": "period_qualifier", "properties": {"max": 1}}
                ]
            }
        }
    )
    return change_date


def get_change_measure():
    change_measure = deepcopy(get_base_measure())
    change_measure.update(
        {
            "max": 3,
            "rules": {
                "0": [
                    {"input": "dimension", "properties": {"min": 0, "max": 1}},
                    {"input": "qualifier", "properties": {"min": 0, "max": 0}}
                ],
                "1": [
                    {"input": "qualifier", "advanced": [
                        {"inputs": [{"name": "date", "selected": 1},
                                    {"name": "dimension", "selected": 1}], "properties": {"min": 0, "max": 1}},
                        {"inputs": [{"name": "date", "selected": 1},
                                    {"name": "focus_on_1", "selected": 1}], "properties": {"min": 0, "max": 0}}
                    ]},
                    {"input": "date", "properties": {"min": 1, "max": 1}},
                    {"input": "dimension", "properties": {"min": 0, "max": 1}},
                ]
            }
        }
    )
    return change_measure


def get_change_dimension():
    change_dimension = deepcopy(get_base_dimension())
    change_dimension.update(
        {
            "max": 2,
            "rules": {
                "0": [
                    {"input": "date", "properties": {"min": 1}},
                    {"input": "measure", "properties": {"min": 1}},
                    {"input": "qualifier", "properties": {"min": 0, "max": 0}}
                ],
                "1": [
                    {"input": "date", "properties": {"min": 1, "max": 1}},
                    {"input": "measure", "properties": {"min": 1}},
                    {"input": "qualifier", "properties": {"min": 0, "max": 1}},
                    {"input": "focus_on", "properties": {"max": 1}}
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
                        "0": [{"input": "qualifier", "advanced": [
                            {"inputs": [{"name": "measure", "selected": 1},
                                        {"name": "dimension", "selected": 1}], "properties": {"min": 0, "max": 1}},
                            {"inputs": [{"name": "measure", "selected": 1},
                                        {"name": "dimension", "selected": 0}], "properties": {"min": 0, "max": 0}}
                        ]}],
                        "1": [{"input": "qualifier", "properties": {"max": 0}}]
                    },
                    "get_values": True,
                    "label": "Focus On",
                    "min": 0,
                    "description": "",
                    "spread": True,
                    "sections": [get_focus_on_sections()['variable'], get_focus_on_sections()['column']]
                }
            ],
        }
    )
    return change_dimension


def get_change():
    return {
        "name": "change",
        "label": "Change",
        "description": "",
        "inputs": [
            get_change_date(),
            get_change_measure(),
            get_change_dimension(),
            get_base_qualifier(),
            get_change_period()
        ]
    }
