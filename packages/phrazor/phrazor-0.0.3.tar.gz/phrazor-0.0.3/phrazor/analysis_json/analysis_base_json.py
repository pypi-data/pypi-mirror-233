def get_base_date():
    return {
        "name": "date",
        "supported_types": [
            "timestamp"
        ],
        "max": 1,
        "label": "Date",
        "min": 1,
        "spread": True,
        "description": "",
        "type": "data",
        "rules": {
            "0": [{"input": "period_qualifier", "properties": {"max": 0}},
                  {"input": "focus_on", "properties": {"max": 0}},
                  {"input": "focus_on_1", "properties": {"max": 0}},
                  {"input": "focus_on_2", "properties": {"max": 0}}],
            "1": [{"input": "period_qualifier", "properties": {"max": 1}},
                  {"input": "focus_on", "properties": {"max": 1}},
                  {"input": "focus_on_1", "properties": {"max": 1}},
                  {"input": "focus_on_2", "properties": {"max": 1}}],
        }
    }


def get_base_measure():
    return {
        "name": "measure",
        "aggregation": True,
        "supported_types": [
            "timestamp",
            "numeric",
            "text"
        ],
        "max": 1,
        "label": "Measure",
        "spread": False,
        "min": 1,
        "description": "",
        "type": "data",
        "rules": {}
    }


def get_focus_on_sections():
    return {
        'variable': {
            'label': 'My Variables',
            'type': 'variable'
        },
        'static': {
            'label': 'Static',
            'type': 'static',
            'options': [
                {
                    'label': 'All',
                    'value': 'all',
                    'name': 'all',
                },
                {
                    'label': 'Others',
                    'value': 'others',
                    'name': 'others'
                }
            ],
        },
        'column': {
            'label': 'Specific Values',
            'type': 'column',
            'max': -1
        }
    }


def get_base_dimension():
    return {
        "name": "dimension",
        "supported_types": [
            "text"
        ],
        "max": 1,
        "label": "Dimension",
        "min": 0,
        "description": "",
        "spread": True,
        "nested": [
            {
                "name": "focus_on",
                "supported_types": [
                    "text", "variable"
                ],
                "max": 1,
                "rules": {
                    "0": [{"input": "qualifier", "properties": {"max": 1}}],
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
        "type": "data",
        "rules": {
            "0": [{"input": "qualifier", "properties": {"max": 0}},
                  {"input": "hierarchy", "properties": {"max": 0}}],
            "1": [{"input": "qualifier", "properties": {"max": 1}},
                  {"input": "hierarchy", "properties": {"max": 0}}],
            "2": [{"input": "qualifier", "properties": {"max": 1}}]
        }
    }


def get_base_qualifier():
    return {
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
            },
            {
                "label": "Top",
                "value": "top_n",
                "key": "qualifier",
                "nested": [{
                    "name": "n_values",
                    "min": 1,
                    "default": 5,
                    "type": "number"
                }]
            },
            {
                "label": "Bottom",
                "value": "bottom_n",
                "key": "qualifier",
                "nested": [{
                    "name": "n_values",
                    "min": 1,
                    "default": 5,
                    "type": "number"
                }]
            }
        ]
    }


def get_static_focus_on_mapping():
    return {
        'all': {
            'formula': "Keys(GroupByCategory(``dimension``, ``primary_metric``, primary_metric_operation))",
            'name': 'all',
            'label': 'All'
        },
        'others': {
            'formula': "RightUnique(focus_on_1, Keys(GroupByCategory(``dimension``, ``primary_metric``, primary_metric_operation)))",
            'name': 'others',
            'label': 'Others',

        }
    }


def get_base_period():
    return {
        "name": "period_qualifier",
        "max": 0,
        "type": "radio",
        "advanced": True,
        "label": "Period Focus",
        "spread": True,
        "options": [
            {
                "label": "Current Period",
                "value": {
                    "formula": "LatestPeriods(``date``, ChangeCase(period,\"lower\"), 1, custom_start_period)",
                    "label": "Current Period",
                    "name": "current_period",
                },

            },
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


def get_base_hierarchy():
    return {
        "name": "hierarchy",
        "type": "custom",
        "label": "Hierarchy",
        "mandatory_inputs": False,
        "advanced": True,
        "spread": True,
        "max": 1,
        "min": 0,
    }


def get_base_period_frame():
    return {
        "name": "period_frame",
        "type": "custom",
        "label": "Compare Period",
        "icon": "far fa-calendar-alt",
        "min": 0,
        "max": 0,
        "spread": True,
        "period": {
            "day": {
                "options": [
                    {
                        "label": "Today with Yesterday",
                        "value": "today_vs_yesterday"
                    }
                ]
            },
            "week": {
                "options": [
                    {
                        "label": "This week with previous week",
                        "value": "current_week_vs_previous_week"
                    },
                    {
                        "label": "Week (This Month) with Week (Previous Month)",
                        "value": "week_this_month_vs_week_previous_month"
                    },
                    {
                        "label": "Week (This Year) with Week (Previous Year)",
                        "value": "week_this_year_vs_week_previous_year"
                    }
                ]
            },
            "wtd": {
                "options": [
                    {
                        "label": "WTD (This month) with WTD (Previous Month)",
                        "value": "wtd_this_month_vs_wtd_previous_month"
                    }
                ]
            },
            "month": {
                "options": [
                    {
                        "label": "This month with previous month",
                        "value": "current_month_vs_previous_month"
                    },
                    {
                        "label": "Month (This Quarter) with Month (Previous Quarter)",
                        "value": "month_this_quarter_vs_month_previous_quarter"
                    },
                    {
                        "label": "Month (This Year) with Month (Previous Year)",
                        "value": "month_this_year_vs_month_previous_year"
                    }
                ]
            },
            "mtd": {
                "options": [
                    {
                        "label": "MTD (This Year) with MTD (Previous Year)",
                        "value": "mtd_this_year_vs_mtd_previous_year"
                    }
                ]
            },
            "quarter": {
                "options": [
                    {
                        "label": "This quarter with previous quarter",
                        "value": "current_quarter_vs_previous_quarter"
                    },
                    {
                        "label": "Quarter (This Year) with Quarter (Previous Year)",
                        "value": "quarter_this_year_vs_quarter_previous_year"
                    }
                ]
            },
            "qtd": {
                "options": [
                    {
                        "label": "QTD (This Year) with QTD (Previous Year)",
                        "value": "qtd_this_year_vs_qtd_previous_year"
                    }
                ]
            },
            "year": {
                "options": [
                    {
                        "label": "This year with previous year",
                        "value": "current_year_vs_previous_year"
                    }
                ]
            },
            "fy": {
                "options": [
                    {
                        "label": "This FY with previous FY",
                        "value": "current_fy_vs_previous_fy"
                    }
                ]
            },
            "ytd": {
                "options": [
                    {
                        "label": "YTD (This Year) with YTD (Previous Year)",
                        "value": "ytd_this_year_vs_ytd_previous_year"
                    }
                ]
            }
        }
    }
