from copy import deepcopy

from phrazor.analysis_json.analysis_base_json import (
    get_base_date, get_base_dimension, get_base_measure,
    get_base_period, get_base_qualifier, get_focus_on_sections
)


def get_descriptor_date():
    descriptor_date = deepcopy(get_base_date())
    descriptor_date.update(
        {
            'min': 0,
            "rules": {
                "0": [
                    {"input": "dimension", "properties": {"min": 0}},
                    {"input": "period_qualifier", "properties": {"max": 0}},
                    {"input": "focus_on", "properties": {"max": 0}}
                ],
                "1": [
                    {"input": "dimension", "properties": {"min": 0}},
                    {"input": "focus_on", "properties": {"max": 1}},
                    {"input": "period_qualifier", "properties": {"max": 1}},
                    {"input": "qualifier", "advanced": [
                        {"inputs": [{"name": "dimension", "selected": 1},
                                    {"name": "measure", "selected": 1},
                                    {"name": "focus_on", "selected": 0}], "properties": {"min": 0, "max": 1}},
                        {"inputs": [{"name": "dimension", "selected": 1},
                                    {"name": "measure", "selected": 1},
                                    {"name": "focus_on", "selected": 1}], "properties": {"min": 0, "max": 0}},
                        {"inputs": [{"name": "dimension", "selected": 0}], "properties": {"min": 0, "max": 0}}
                    ]},
                ]
            }
        }
    )
    return descriptor_date


def get_descriptor_measure():
    descriptor_measure = deepcopy(get_base_measure())
    descriptor_measure.update(
        {
            "max": 3,
            "rules": {
                "0": [
                    {"input": "dimension", "properties": {"min": 0, "max": 1}},
                    {"input": "qualifier", "properties": {"min": 0, "max": 0}}
                ],
                "1": [
                    {"input": "qualifier", "advanced": [
                        {"inputs": [{"name": "dimension", "selected": 1}], "properties": {"min": 0, "max": 1}},
                        {"inputs": [{"name": "dimension", "selected": 0}], "properties": {"min": 0, "max": 0}}
                    ]},
                    {"input": "date", "advanced": [
                        {"inputs": [{"name": "dimension", "selected": 1}], "properties": {"min": 0, "max": 1}},
                        {"inputs": [{"name": "dimension", "selected": 0}], "properties": {"min": 0, "max": 1}}
                    ]},
                    {"input": "dimension", "properties": {"min": 0, "max": 1}},
                ]
            }
        }
    )
    return descriptor_measure


def get_descriptor_dimension():
    descriptor_dimension = deepcopy(get_base_dimension())
    descriptor_dimension.update(
        {
            "max": 2,
            "rules": {
                "0": [
                    {"input": "date", "properties": {"min": 0}},
                    {"input": "measure", "properties": {"min": 1}},
                    {"input": "qualifier", "properties": {"min": 0, "max": 0}}
                ],
                "1": [
                    {"input": "date", "properties": {"min": 0}},
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
    return descriptor_dimension


def get_descriptor():
    return {
        "name": "descriptor",
        "label": "Descriptor",
        "description": "",
        "inputs": [
            get_descriptor_date(),
            get_descriptor_measure(),
            get_descriptor_dimension(),
            get_base_qualifier(),
            get_base_period()
        ]
    }
