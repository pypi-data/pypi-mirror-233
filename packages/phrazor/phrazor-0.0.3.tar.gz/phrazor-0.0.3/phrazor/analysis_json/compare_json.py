from copy import deepcopy

from phrazor.analysis_json.analysis_base_json import (
    get_base_date, get_base_dimension, get_base_measure,
    get_base_period, get_base_period_frame, get_base_qualifier, get_focus_on_sections
)


def get_compare_qualifier():
    compare_qualifier = deepcopy(get_base_qualifier())
    compare_qualifier.update(
        {
            "name": "qualifier",
            "max": 0,
            "type": "radio",
            "advanced": True,
            "label": "Dimension Focus",
            "spread": True,
            "options": [
                {
                    "label": "Highest",
                    "value": "highest",
                    "key": "qualifier",
                    "nested": [{
                        "name": "n_values",
                        "min": 1,
                        "default": 1,
                        "type": "number",
                        "show": False
                    }]
                },
                {
                    "label": "Lowest",
                    "value": "lowest",
                    "key": "qualifier",
                    "nested": [{
                        "name": "n_values",
                        "min": 1,
                        "default": 1,
                        "type": "number",
                        "show": False
                    }]
                }
            ]
        }
    )
    return compare_qualifier


def get_compare_date():
    compare_date = deepcopy(get_base_date())
    compare_date.update(
        {
            "mandatory_inputs": False,
            "rules": {
                "0": [{"input": "period_qualifier", "properties": {"max": 0}}],
                "1": [{"input": "period_qualifier", "properties": {"max": 1}}]
            }

        }
    )
    return compare_date


def get_compare_measure():
    compare_measure = deepcopy(get_base_measure())
    compare_measure.update(
        {
            "max": 2,
            "rules": {
                "0": [
                    {"input": "period_qualifier", "properties": {"max": 0}},
                    {"input": "qualifier", "properties": {"max": 0}},
                    {"input": "focus_on_1", "properties": {"max": 0}},
                    {"input": "focus_on_2", "properties": {"max": 0}}
                ],
                "1": [
                    {"input": "date", "properties": {"min": 1}},
                    {"input": "period_frame", "advanced": [
                        {"inputs": [{"name": "focus_on_1", "selected": 1}], "properties": {"min": 1, "max": 1}},
                        {"inputs": [{"name": "focus_on_1", "selected": 0}], "properties": {"min": 0, "max": 0}},
                    ]},
                    {"input": "period_qualifier", "advanced": [
                        {"inputs": [{"name": "focus_on_1", "selected": 1}], "properties": {"min": 0, "max": 0}},
                        {"inputs": [{"name": "focus_on_1", "selected": 0}], "properties": {"min": 0, "max": 1}},
                    ]},
                    {"input": "qualifier", "properties": {"min": 0, "max": 0}},
                    {"input": "focus_on_1", "properties": {"min": 1, "max": 1}},
                    {"input": "focus_on_2", "properties": {"max": 1}}
                ],
                "2": [
                    {"input": "date", "properties": {"min": 1}},
                    {"input": "period_frame", "properties": {"min": 0, "max": 0}},
                    {"input": "period_qualifier", "properties": {"min": 0, "max": 1}},
                    {"input": "qualifier", "advanced": [
                        {"inputs": [{"name": "focus_on_1", "selected": 1}], "properties": {"min": 0, "max": 0}},
                        {"inputs": [{"name": "dimension", "selected": 1},
                                    {"name": "focus_on_1", "selected": 0}], "properties": {"min": 0, "max": 1}},
                        {"inputs": [{"name": "dimension", "selected": 0}], "properties": {"min": 0, "max": 0}}
                    ]},
                    {"input": "dimension", "properties": {"min": 0, "max": 1}},
                    {"input": "focus_on_1", "properties": {"min": 0, "max": 1}},
                    {"input": "focus_on_2", "properties": {"max": 0}}
                ]
            }
        }
    )
    return compare_measure


def get_compare_dimension():
    compare_dimension = deepcopy(get_base_dimension())
    compare_dimension.update(
        {
            "mandatory_inputs": False,
            "rules": {
                "0": [{"input": "qualifier", "properties": {"min": 0, "max": 0}},
                      {"input": "measure", "properties": {"min": 2}},
                      {"input": "period_frame", "advanced": [
                          {"inputs": [{"name": "measure", "selected": 1}], "properties": {"min": 0, "max": 0}},
                          {"inputs": [{"name": "measure", "selected": 2}], "properties": {"min": 0, "max": 0}},
                      ]}
                      ],
                "1": [{"input": "qualifier", "advanced": [
                    {"inputs": [{"name": "measure", "selected": 1}], "properties": {"min": 0, "max": 0}},
                    {"inputs": [{"name": "measure", "selected": 2}], "properties": {"min": 0, "max": 1}}
                ]},
                      {"input": "focus_on_1", "advanced": [
                          {"inputs": [{"name": "measure", "selected": 1}], "properties": {"min": 1, "max": 1}},
                          {"inputs": [{"name": "measure", "selected": 2}], "properties": {"min": 0}},
                      ]},
                      {"input": "measure", "properties": {"min": 1}},
                      {"input": "period_qualifier", "properties": {"max": 1}}],
                "2": [{"input": "qualifier", "properties": {"max": 1}},
                      {"input": "period_qualifier", "properties": {"max": 0}}]
            },
            "nested": [
                {
                    "name": "focus_on_1",
                    "supported_types": [
                        "text", "variable"
                    ],
                    "max": 1,
                    "rules": {
                        "0": [
                            {"input": "period_frame", "properties": {"min": 0, "max": 0}},
                            {"input": "period_qualifier", "properties": {"max": 1}},
                            {"input": "qualifier", "advanced": [
                                {"inputs": [{"name": "measure", "selected": 1}], "properties": {"min": 0, "max": 0}},
                                {"inputs": [{"name": "measure", "selected": 2},
                                            {"name": "dimension", "selected": 1}], "properties": {"min": 0, "max": 1}},
                                {"inputs": [{"name": "measure", "selected": 2},
                                            {"name": "dimension", "selected": 0}], "properties": {"min": 0, "max": 0}}
                            ]},
                            {"input": "measure", "properties": {"min": 2}}],
                        "1": [{"input": "date", "advanced": [
                            {"inputs": [{"name": "measure", "selected": 2}], "properties": {"min": 1, "max": 1}},
                            {"inputs": [{"name": "measure", "selected": 1}], "properties": {"min": 1, "max": 1}}
                        ]},
                              {"input": "measure", "properties": {"min": 1, "max": 2}},
                              {"input": "period_qualifier", "advanced": [
                                  {"inputs": [{"name": "measure", "selected": 2}], "properties": {"max": 1}},
                                  {"inputs": [{"name": "measure", "selected": 1}], "properties": {"min": 0, "max": 0}}
                              ]},
                              {"input": "qualifier", "properties": {"min": 0, "max": 0}},
                              {"input": "period_frame", "advanced": [
                                  {"inputs": [{"name": "measure", "selected": 2}], "properties": {"min": 0, "max": 0}},
                                  {"inputs": [{"name": "measure", "selected": 1}], "properties": {"min": 1, "max": 1}}
                              ]}]
                    },
                    "get_values": True,
                    "label": None,
                    "mandatory_inputs": True,
                    "description": "",
                    "spread": True,
                    "sections": [get_focus_on_sections()['variable'], get_focus_on_sections()['column']]
                },
                {
                    "name": "focus_on_2",
                    "supported_types": [
                        "text", "variable"
                    ],
                    "max": 1,
                    "rules": {
                        "0": [{"input": "measure", "properties": {"max": 2}},
                              {"input": "period_qualifier", "properties": {"min": 0, "max": 0}},
                              {"input": "period_frame", "advanced": [
                                  {"inputs": [{"name": "measure", "selected": 1},
                                              {"name": "focus_on_1", "selected": 1}],
                                   "properties": {"min": 1, "max": 1}},
                                  {"inputs": [{"name": "measure", "selected": 1},
                                              {"name": "focus_on_1", "selected": 0}],
                                   "properties": {"min": 0, "max": 0}},
                                  {"inputs": [{"name": "measure", "selected": 2}], "properties": {"min": 0, "max": 0}}
                              ]}],
                        "1": [{"input": "date", "properties": {"min": 0, "max": 1}},
                              {"input": "measure", "properties": {"max": 1}},
                              {"input": "period_qualifier", "properties": {"max": 1}},
                              {"input": "qualifier", "properties": {"min": 0, "max": 0}},
                              {"input": "period_frame", "properties": {"min": 0, "max": 0}}]
                    },
                    "get_values": True,
                    "label": None,
                    "mandatory_inputs": False,
                    "description": "",
                    "spread": True,
                    "sections": [get_focus_on_sections()['variable'], get_focus_on_sections()['column'],
                                 get_focus_on_sections()['static']]
                }
            ]
        }
    )
    return compare_dimension


def get_compare_single_dimension():
    compare_single_dimension = deepcopy(get_base_dimension())
    compare_single_dimension.update(
        {
            "mandatory_inputs": False,
            "rules": {
                "0": [{"input": "qualifier", "properties": {"min": 0, "max": 0}},
                      {"input": "measure", "properties": {"min": 2}},
                      {"input": "period_frame", "advanced": [
                          {"inputs": [{"name": "measure", "selected": 1}], "properties": {"min": 0, "max": 0}},
                          {"inputs": [{"name": "measure", "selected": 2}], "properties": {"min": 0, "max": 0}},
                      ]}
                      ],
                "1": [{"input": "qualifier", "advanced": [
                    {"inputs": [{"name": "measure", "selected": 1}], "properties": {"min": 0, "max": 0}},
                    {"inputs": [{"name": "measure", "selected": 2}], "properties": {"min": 0, "max": 1}}
                ]},
                      {"input": "focus_on_1", "advanced": [
                          {"inputs": [{"name": "measure", "selected": 1}], "properties": {"min": 1, "max": 1}},
                          {"inputs": [{"name": "measure", "selected": 2}], "properties": {"min": 0}},
                      ]},
                      {"input": "measure", "properties": {"min": 1}},
                      {"input": "period_qualifier", "properties": {"max": 1}}],
                "2": [{"input": "qualifier", "properties": {"max": 1}},
                      {"input": "period_qualifier", "properties": {"max": 0}}]
            },
            "nested": [
                {
                    "name": "focus_on_1",
                    "supported_types": [
                        "text", "variable"
                    ],
                    "min": 0,
                    "max": 1,
                    "rules": {
                        "0": [
                            {"input": "period_frame", "properties": {"min": 0, "max": 0}},
                            {"input": "period_qualifier", "properties": {"max": 1}},
                            {"input": "qualifier", "advanced": [
                                {"inputs": [{"name": "measure", "selected": 1}], "properties": {"min": 0, "max": 0}},
                                {"inputs": [{"name": "measure", "selected": 2},
                                            {"name": "dimension", "selected": 1}], "properties": {"min": 0, "max": 1}},
                                {"inputs": [{"name": "measure", "selected": 2},
                                            {"name": "dimension", "selected": 0}], "properties": {"min": 0, "max": 0}}
                            ]},
                            {"input": "measure", "properties": {"min": 2}}],
                        "1": [{"input": "date", "advanced": [
                            {"inputs": [{"name": "measure", "selected": 2}], "properties": {"min": 1, "max": 1}},
                            {"inputs": [{"name": "measure", "selected": 1}], "properties": {"min": 1, "max": 1}}
                        ]},
                              {"input": "measure", "properties": {"min": 1, "max": 2}},
                              {"input": "period_qualifier", "advanced": [
                                  {"inputs": [{"name": "measure", "selected": 2}], "properties": {"max": 1}},
                                  {"inputs": [{"name": "measure", "selected": 1}], "properties": {"min": 0, "max": 0}}
                              ]},
                              {"input": "qualifier", "properties": {"min": 0, "max": 0}},
                              {"input": "period_frame", "advanced": [
                                  {"inputs": [{"name": "measure", "selected": 2}], "properties": {"min": 0, "max": 0}},
                                  {"inputs": [{"name": "measure", "selected": 1}], "properties": {"min": 1, "max": 1}}
                              ]}]
                    },
                    "get_values": True,
                    "label": None,
                    "mandatory_inputs": True,
                    "description": "",
                    "spread": True,
                    "sections": [get_focus_on_sections()['variable'], get_focus_on_sections()['column']]
                }
            ]
        }
    )
    return compare_single_dimension


def get_compare_single_measure():
    compare_single_measure = deepcopy(get_base_measure())
    compare_single_measure.update(
        {
            "max": 1,
            "rules": {
                "0": [
                    {"input": "period_qualifier", "properties": {"max": 0}},
                    {"input": "qualifier", "properties": {"max": 0}},
                    {"input": "focus_on_1", "properties": {"max": 0}},
                    {"input": "focus_on_2", "properties": {"max": 0}}
                ],
                "1": [
                    {"input": "date", "properties": {"min": 1}},
                    {"input": "period_frame", "advanced": [
                        {"inputs": [{"name": "focus_on_1", "selected": 1}], "properties": {"min": 1, "max": 1}},
                        {"inputs": [{"name": "focus_on_1", "selected": 0}], "properties": {"min": 0, "max": 0}},
                    ]},
                    {"input": "period_qualifier", "advanced": [
                        {"inputs": [{"name": "focus_on_1", "selected": 1}], "properties": {"min": 0, "max": 0}},
                        {"inputs": [{"name": "focus_on_1", "selected": 0}], "properties": {"min": 0, "max": 1}},
                    ]},
                    {"input": "qualifier", "properties": {"min": 0, "max": 0}},
                    {"input": "focus_on_1", "properties": {"min": 1, "max": 1}},
                    {"input": "focus_on_2", "properties": {"max": 1}}
                ],
                "2": [
                    {"input": "date", "properties": {"min": 1}},
                    {"input": "period_frame", "properties": {"min": 0, "max": 0}},
                    {"input": "period_qualifier", "properties": {"min": 0, "max": 1}},
                    {"input": "qualifier", "advanced": [
                        {"inputs": [{"name": "focus_on_1", "selected": 1}], "properties": {"min": 0, "max": 0}},
                        {"inputs": [{"name": "dimension", "selected": 1},
                                    {"name": "focus_on_1", "selected": 0}], "properties": {"min": 0, "max": 1}},
                        {"inputs": [{"name": "dimension", "selected": 0}], "properties": {"min": 0, "max": 0}}
                    ]},
                    {"input": "dimension", "properties": {"min": 0, "max": 1}},
                    {"input": "focus_on_1", "properties": {"min": 0, "max": 1}},
                    {"input": "focus_on_2", "properties": {"max": 0}}
                ]
            }
        }
    )
    return compare_single_measure


def get_compare_double_dimension():
    compare_double_dimension = deepcopy(get_compare_dimension())
    compare_double_dimension.update(
        {
            "min": 1,
        }
    )
    return compare_double_dimension


def get_compare_double_measure():
    compare_double_measure = deepcopy(get_compare_measure())
    compare_double_measure.update(
        {
            "min": 2
        }
    )
    return compare_double_measure


def get_measure_compare():
    return {
        "name": "compare",
        "label": "Compare Measures",
        "description": "",
        "inputs": [
            get_compare_date(),
            get_compare_double_measure(),
            get_compare_single_dimension(),
            get_base_period_frame(),
            get_compare_qualifier(),
            get_base_period()
        ]
    }


def get_dimension_compare():
    return {
        "name": "compare",
        "label": "Compare Dimension Values",
        "description": "",
        "inputs": [
            get_compare_date(),
            get_compare_single_measure(),
            get_compare_double_dimension(),
            get_base_period_frame(),
            get_compare_qualifier(),
            get_base_period()
        ]
    }
