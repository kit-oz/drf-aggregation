from datetime import date, datetime, timedelta, timezone

ANNOTATIONS_TESTING = [
    ({"aggregations": {"value": {"type": "count"}}}, {"value": 6}),
    (
        {
            "aggregations": {
                "value": {"type": "sum", "field": "integer"},
            }
        },
        {"value": 15},
    ),
    (
        {
            "aggregations": {
                "value": {"type": "average", "field": "integer"},
            }
        },
        {"value": 2.5},
    ),
    (
        {"aggregations": {"value": {"type": "minimum", "field": "integer"}}},
        {"value": 0},
    ),
    (
        {"aggregations": {"value": {"type": "maximum", "field": "integer"}}},
        {"value": 5},
    ),
    (
        {
            "aggregations": {
                "value": {
                    "type": "percentile",
                    "field": "integer",
                    "percentile": 0.5,
                }
            }
        },
        {"value": 2.5},
    ),
    (
        {"aggregations": {"value": {"type": "sum", "field": "float"}}},
        {"value": 15},
    ),
    (
        {"aggregations": {"value": {"type": "average", "field": "float"}}},
        {"value": 2.5},
    ),
    (
        {"aggregations": {"value": {"type": "minimum", "field": "float"}}},
        {"value": 0},
    ),
    (
        {"aggregations": {"value": {"type": "maximum", "field": "float"}}},
        {"value": 5},
    ),
    (
        {
            "aggregations": {
                "value": {
                    "type": "percentile",
                    "field": "float",
                    "percentile": 0.5,
                }
            }
        },
        {"value": 2.5},
    ),
    (
        {"aggregations": {"value": {"type": "minimum", "field": "date"}}},
        {"value": date(2020, 10, 1)},
    ),
    (
        {"aggregations": {"value": {"type": "maximum", "field": "date"}}},
        {"value": date(2020, 11, 2)},
    ),
    (
        {"aggregations": {"value": {"type": "minimum", "field": "datetime"}}},
        {"value": datetime(2020, 10, 1, 0, 1, tzinfo=timezone.utc)},
    ),
    (
        {"aggregations": {"value": {"type": "maximum", "field": "datetime"}}},
        {"value": datetime(2020, 11, 2, 0, 6, tzinfo=timezone.utc)},
    ),
    (
        {"aggregations": {"value": {"type": "sum", "field": "duration"}}},
        {"value": timedelta(days=21)},
    ),
    (
        {"aggregations": {"value": {"type": "average", "field": "duration"}}},
        {"value": timedelta(days=3, hours=12)},
    ),
    (
        {"aggregations": {"value": {"type": "minimum", "field": "duration"}}},
        {"value": timedelta(days=1)},
    ),
    (
        {"aggregations": {"value": {"type": "maximum", "field": "duration"}}},
        {"value": timedelta(days=6)},
    ),
    (
        {
            "aggregations": {
                "value": {
                    "type": "percentile",
                    "field": "duration",
                    "percentile": 0.5,
                }
            }
        },
        {"value": timedelta(days=3, hours=12)},
    ),
    (
        {
            "aggregations": {
                "value": {
                    "type": "percent",
                    "additional_filter": {
                        "type": "operator",
                        "data": {
                            "attribute": "group2",
                            "operator": "=",
                            "value": "1",
                        },
                    },
                }
            }
        },
        {"value_numerator": 3, "value_denominator": 6, "value": 0.5},
    ),
]

UNSORTED_GROUPS_TESTING = [
    # GROUP BY ONE FIELD
    (
        {
            "aggregations": {
                "value": {
                    "type": "count",
                }
            },
            "group_by": "group1",
        },
        [
            {"group1": "1", "value": 2},
            {"group1": "2", "value": 1},
            {"group1": "3", "value": 3},
        ],
    ),
    # GROUP BY MULTIPLE FIELDS
    (
        {
            "aggregations": {
                "value": {
                    "type": "count",
                }
            },
            "group_by": "group1,group2",
        },
        [
            {"group1": "3", "group2": "3", "value": 1},
            {"group1": "3", "group2": "2", "value": 1},
            {"group1": "1", "group2": "2", "value": 1},
            {"group1": "2", "group2": "1", "value": 1},
            {"group1": "3", "group2": "1", "value": 1},
            {"group1": "1", "group2": "1", "value": 1},
        ],
    ),
    # IGNORE LIMIT BY AND SHOW OTHER WITHOUT LIMIT
    (
        {
            "aggregations": {
                "value": {
                    "type": "count",
                }
            },
            "group_by": "group1",
            "limit_by": "group1",
            "showOther": True,
        },
        [
            {"group1": "1", "value": 2},
            {"group1": "2", "value": 1},
            {"group1": "3", "value": 3},
        ],
    ),
]

SORTED_GROUPS_TESTING = [
    # DESCENDING SORTING BY VALUE
    (
        {
            "aggregations": {
                "value": {
                    "type": "count",
                }
            },
            "group_by": "group1",
            "order_by": "-value",
        },
        [
            {"group1": "3", "value": 3},
            {"group1": "1", "value": 2},
            {"group1": "2", "value": 1},
        ],
    ),
    # ASCENDING SORTING BY VALUE
    (
        {
            "aggregations": {
                "value": {
                    "type": "count",
                }
            },
            "group_by": "group1",
            "order_by": "value",
        },
        [
            {"group1": "2", "value": 1},
            {"group1": "1", "value": 2},
            {"group1": "3", "value": 3},
        ],
    ),
    # SORT BY GROUP NAME
    (
        {
            "aggregations": {
                "value": {
                    "type": "count",
                }
            },
            "group_by": "group1",
            "order_by": "group1",
        },
        [
            {"group1": "1", "value": 2},
            {"group1": "2", "value": 1},
            {"group1": "3", "value": 3},
        ],
    ),
    # GROUP BY MULTIPLE FIELDS WITH SORT BY TOTAL GROUP VALUE
    (
        {
            "columnIndex": "group1",
            "aggregations": {
                "value": {
                    "type": "count",
                }
            },
            "group_by": "group1,group2",
            "order_by": "-group1__index,-group2",
        },
        [
            {"group1": "3", "group2": "3", "value": 1},
            {"group1": "3", "group2": "2", "value": 1},
            {"group1": "3", "group2": "1", "value": 1},
            {"group1": "1", "group2": "2", "value": 1},
            {"group1": "1", "group2": "1", "value": 1},
            {"group1": "2", "group2": "1", "value": 1},
        ],
    ),
    # LIMIT NUMBER OF RETURNED GROUPS
    (
        {
            "aggregations": {
                "value": {
                    "type": "count",
                }
            },
            "group_by": "group1",
            "order_by": "-value",
            "limit": 1,
        },
        [{"group1": "3", "value": 3}],
    ),
    # LIMIT WITH GROUP BY MULTIPLE FIELDS
    (
        {
            "columnIndex": "group1",
            "aggregations": {
                "value": {
                    "type": "count",
                }
            },
            "group_by": "group1,group2",
            "order_by": "-group1__index,-group2",
            "limit": 1,
        },
        [
            {"group1": "3", "group2": "3", "value": 1},
            {"group1": "3", "group2": "2", "value": 1},
            {"group1": "3", "group2": "1", "value": 1},
        ],
    ),
    # LIMIT WITH GROUP BY MULTIPLE FIELDS AND SHOW OTHER
    (
        {
            "columnIndex": "group1",
            "aggregations": {
                "value": {
                    "type": "count",
                }
            },
            "group_by": "group1,group2",
            "order_by": "-group1__index,-group2",
            "limit": 1,
            "showOther": True,
        },
        [
            {"group1": "3", "group2": "3", "value": 1},
            {"group1": "3", "group2": "2", "value": 1},
            {"group1": "3", "group2": "1", "value": 1},
            {"group1": "Other", "group2": "2", "value": 1},
            {"group1": "Other", "group2": "1", "value": 2},
        ],
    ),
    # LIMIT BY NOT FIRST FIELD IN GROUP BY
    (
        {
            "columnIndex": "group2",
            "aggregations": {
                "value": {
                    "type": "count",
                }
            },
            "group_by": "group1,group2",
            "order_by": "group2__index",
            "limit": 1,
            "limit_by": "group2",
        },
        [{"group1": "3", "group2": "3", "value": 1}],
    ),
    # LIMIT NUMBER OF RETURNED GROUPS, WITH GROUP "OTHER"
    (
        {
            "aggregations": {
                "value": {
                    "type": "count",
                }
            },
            "group_by": "group1",
            "order_by": "-value",
            "limit": 1,
            "showOther": True,
        },
        [{"group1": "3", "value": 3}, {"group1": "Other", "value": 3}],
    ),
    # NOT SHOW EMPTY GROUP "OTHER"
    (
        {
            "aggregations": {
                "value": {
                    "type": "count",
                },
            },
            "group_by": "group1",
            "order_by": "-value",
            "limit": 3,
            "showOther": True,
        },
        [
            {"group1": "3", "value": 3},
            {"group1": "1", "value": 2},
            {"group1": "2", "value": 1},
        ],
    ),
    # GROUP BY PERCENT AGGREGATION
    (
        {
            "aggregations": {
                "value": {
                    "type": "percent",
                    "additional_filter": {
                        "type": "operator",
                        "data": {
                            "attribute": "group2",
                            "operator": "=",
                            "value": "2",
                        },
                    },
                }
            },
            "group_by": "group1",
            "order_by": "-value",
        },
        [
            {"group1": "1", "value_numerator": 1, "value_denominator": 2, "value": 0.5},
            {
                "group1": "3",
                "value_numerator": 1,
                "value_denominator": 3,
                "value": 1 / 3,
            },
            {"group1": "2", "value_numerator": 0, "value_denominator": 1, "value": 0},
        ],
    ),
    # SORT BY DATE FIELD
    (
        {
            "aggregations": {
                "value": {
                    "type": "count",
                }
            },
            "truncateDate": "date=day",
            "group_by": "date__trunc__day",
            "order_by": "date__trunc__day",
        },
        [
            {"date__trunc__day": date(2020, 10, 1), "value": 2},
            {"date__trunc__day": date(2020, 10, 31), "value": 1},
            {"date__trunc__day": date(2020, 11, 1), "value": 2},
            {"date__trunc__day": date(2020, 11, 2), "value": 1},
        ],
    ),
    # AGGREGATION ON EMPTY QUERY
    (
        {
            "aggregations": {
                "value": {
                    "type": "count",
                }
            },
            "group_by": "group1",
        },
        [],
        {"search": "4"},
    ),
    # AGGREGATION ON EMPTY QUERY WITH SORT BY TOTAL GROUP VALUE
    (
        {
            "columnIndex": "group1",
            "aggregations": {
                "value": {
                    "type": "count",
                }
            },
            "group_by": "group1,group2",
            "order_by": "-group1__index,-group2",
        },
        [],
        {"search": "4"},
    ),
]
