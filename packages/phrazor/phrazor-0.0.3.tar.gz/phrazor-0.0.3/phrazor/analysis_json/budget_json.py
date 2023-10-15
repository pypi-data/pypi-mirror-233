from copy import deepcopy

from phrazor.analysis_json.analysis_base_json import (
    get_base_date, get_base_dimension, get_base_measure,
    get_base_qualifier, get_focus_on_sections
)


def get_budget_date():
    budget_date = deepcopy(get_base_date())
    budget_date.update(
        {
            "mandatory_inputs": False,
            "rules": {
                "0": [{"input": "measure", "properties": {"min": 2, "max": 2}},
                      {"input": "dimension", "properties": {"min": 0, "max": 1}},
                      {"input": "focus_on", "properties": {"min": 0, "max": 1}}
                      ],
                "1": [{"input": "measure", "properties": {"min": 2, "max": 2}},
                      {"input": "dimension", "properties": {"min": 0, "max": 1}},
                      {"input": "focus_on", "properties": {"min": 0, "max": 1}}
                      ]
            }
        }
    )
    return budget_date


def get_budget_primary_metric():
    budget_primary_metric = deepcopy(get_base_measure())
    budget_primary_metric.update(
        {
            "min": 2,
            "max": 2,
            "rules": {
                "0": [{"input": "qualifier", "properties": {"min": 0, "max": 0}}],
                "1": [{"input": "qualifier", "properties": {"min": 0, "max": 0}},
                      {"input": "date", "properties": {"min": 1, "max": 1}}],
                "2": [{"input": "qualifier", "advanced": [{"inputs": [{"name": "dimension", "selected": 1},
                                                                      {"name": "focus_on", "selected": 0}],
                                                           "properties": {"min": 0, "max": 1}}
                                                          ]},
                      {"input": "date", "advanced": [

                          {"inputs": [{"name": "dimension", "selected": 1},
                                      {"name": "focus_on", "selected": 1}], "properties": {"min": 0, "max": 1}}
                      ]
                       },
                      {"input": "date", "advanced": [
                          {"inputs": [{"name": "dimension", "selected": 0}], "properties": {"min": 0, "max": 1}}
                      ]
                       }
                      ]
            }
        }
    )
    return budget_primary_metric


def get_budget_dimension():
    budget_dimension = deepcopy(get_base_dimension())
    budget_dimension.update(
        {
            "rules": {
                "0": [{"input": "qualifier", "properties": {"min": 0, "max": 0}}],
                "1": [{"input": "qualifier", "advanced": [
                    {"inputs": [{"name": "measure", "selected": 1}], "properties": {"min": 0, "max": 0}},
                    {"inputs": [{"name": "", "selected": 1}], "properties": {"min": 0, "max": 0}},
                    {"inputs": [{"name": "measure", "selected": 2},
                                {"name": "focus_on", "selected": 0}], "properties": {"min": 0, "max": 1}}
                ]},
                      {"input": "date", "advanced": [
                          {"inputs": [{"name": "measure", "selected": 1}], "properties": {"min": 1, "max": 1}},
                          {"inputs": [{"name": "", "selected": 1}], "properties": {"min": 0, "max": 1}},
                          {"inputs": [{"name": "measure", "selected": 2},
                                      {"name": "focus_on", "selected": 0}], "properties": {"min": 0, "max": 1}},
                          {"inputs": [{"name": "measure", "selected": 2},
                                      {"name": "focus_on", "selected": 1}], "properties": {"min": 1, "max": 1}}
                      ]},
                      {"input": "focus_on", "properties": {"min": 0, "max": 1}}
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
                                        {"name": "dimension", "selected": 1}], "properties": {"min": 0, "max": 0}},
                            {"inputs": [{"name": "measure", "selected": 2},
                                        {"name": "dimension", "selected": 1}], "properties": {"min": 0, "max": 1}},
                        ]},
                              {"input": "date", "advanced": [
                                  {"inputs": [{"name": "dimension", "selected": 0}],
                                   "properties": {"min": 0, "max": 1}},
                                  {"inputs": [{"name": "dimension", "selected": 1}],
                                   "properties": {"min": 0, "max": 1}},
                              ]}
                              ],
                        "1": [{"input": "qualifier", "properties": {"min": 0, "max": 0}},
                              {"input": "date", "properties": {"min": 1, "max": 1}}
                              ]
                    },
                    "get_values": True,
                    "label": "Focus On",
                    "min": 0,
                    "description": "",
                    "spread": True,
                    "sections": [get_focus_on_sections()['variable'], get_focus_on_sections()['column']]
                }
            ]
        }
    )
    return budget_dimension


def get_budget():
    return {
        "name": "budget_vs_expense",
        "label": "Budget",
        "description": "",
        "inputs": [
            get_budget_date(),
            get_budget_primary_metric(),
            get_budget_dimension(),
            get_base_qualifier()
        ]

    }
