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
        {"value": "2020-10-01"},
    ),
    (
        {"aggregations": {"value": {"type": "maximum", "field": "date"}}},
        {"value": "2020-11-02"},
    ),
    (
        {"aggregations": {"value": {"type": "minimum", "field": "datetime"}}},
        {"value": "2020-10-01T00:01:00Z"},
    ),
    (
        {"aggregations": {"value": {"type": "maximum", "field": "datetime"}}},
        {"value": "2020-11-02T00:06:00Z"},
    ),
    (
        {"aggregations": {"value": {"type": "sum", "field": "duration"}}},
        {"value": "P21DT00H00M00S"},
    ),
    (
        {"aggregations": {"value": {"type": "average", "field": "duration"}}},
        {"value": "P3DT12H00M00S"},
    ),
    (
        {"aggregations": {"value": {"type": "minimum", "field": "duration"}}},
        {"value": "P1DT00H00M00S"},
    ),
    (
        {"aggregations": {"value": {"type": "maximum", "field": "duration"}}},
        {"value": "P6DT00H00M00S"},
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
        {"value": "P3DT12H00M00S"},
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
    (
        {
            "aggregations": {
                "count": {"type": "count"},
                "percent": {
                    "type": "percent",
                    "additional_filter": {
                        "type": "operator",
                        "data": {
                            "attribute": "group2",
                            "operator": "=",
                            "value": "1",
                        },
                    },
                },
            }
        },
        {"count": 6, "percent_numerator": 3, "percent_denominator": 6, "percent": 0.5},
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
    # GROUP BY ONE FIELD WITH MULTIPLE AGGREGATION
    (
        {
            "aggregations": {
                "cnt": {"type": "count"},
                "mx": {"type": "maximum", "field": "integer"},
            },
            "group_by": "group1",
        },
        [
            {"group1": "1", "cnt": 2, "mx": 2},
            {"group1": "2", "cnt": 1, "mx": 0},
            {"group1": "3", "cnt": 3, "mx": 5},
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
    # GROUP BY MULTIPLE FIELDS WITH MULTIPLE AGGREGATION
    (
        {
            "aggregations": {
                "cnt": {"type": "count"},
                "mx": {"type": "maximum", "field": "integer"},
            },
            "group_by": "group1,group2",
        },
        [
            {"group1": "3", "group2": "3", "cnt": 1, "mx": 5},
            {"group1": "3", "group2": "2", "cnt": 1, "mx": 3},
            {"group1": "1", "group2": "2", "cnt": 1, "mx": 1},
            {"group1": "2", "group2": "1", "cnt": 1, "mx": 0},
            {"group1": "3", "group2": "1", "cnt": 1, "mx": 4},
            {"group1": "1", "group2": "1", "cnt": 1, "mx": 2},
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
            "limit": {
                "by_group": "group1",
                "by_aggregation": "value",
                "show_other": True,
            },
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
            "aggregations": {
                "value": {
                    "type": "count",
                    "index_by_group": "group1",
                }
            },
            "group_by": "group1,group2",
            "order_by": "-group1__value,-group2",
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
    # GROUP BY MULTIPLE FIELDS WITH SORT BY TOTAL GROUP VALUE WITH MULTIPLE AGGREGATION
    (
        {
            "aggregations": {
                "value": {
                    "type": "count",
                    "index_by_group": "group1",
                },
                "mx": {"type": "maximum", "field": "integer"},
            },
            "group_by": "group1,group2",
            "order_by": "-group1__value,-group2",
        },
        [
            {"group1": "3", "group2": "3", "value": 1, "mx": 5},
            {"group1": "3", "group2": "2", "value": 1, "mx": 3},
            {"group1": "3", "group2": "1", "value": 1, "mx": 4},
            {"group1": "1", "group2": "2", "value": 1, "mx": 1},
            {"group1": "1", "group2": "1", "value": 1, "mx": 2},
            {"group1": "2", "group2": "1", "value": 1, "mx": 0},
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
            "aggregations": {
                "value": {
                    "type": "count",
                    "index_by_group": "group1",
                }
            },
            "group_by": "group1,group2",
            "order_by": "-group1__value,-group2",
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
            "aggregations": {
                "value": {
                    "type": "count",
                    "index_by_group": "group1",
                }
            },
            "group_by": "group1,group2",
            "order_by": "-group1__value,-group2",
            "limit": {
                "limit": 1,
                "by_group": "group1",
                "by_aggregation": "value",
                "show_other": True,
            },
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
            "aggregations": {
                "value": {
                    "type": "count",
                    "index_by_group": "group2",
                }
            },
            "group_by": "group1,group2",
            "order_by": "group2__value",
            "limit": {
                "limit": 1,
                "by_group": "group2",
                "by_aggregation": "value",
            },
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
            "limit": {
                "limit": 1,
                "show_other": True,
            },
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
            "limit": {
                "limit": 3,
                "show_other": True,
            },
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
            "truncate_rules": {"date": "day"},
            "group_by": "date__trunc__day",
            "order_by": "date__trunc__day",
        },
        [
            {"date__trunc__day": "2020-10-01", "value": 2},
            {"date__trunc__day": "2020-10-31", "value": 1},
            {"date__trunc__day": "2020-11-01", "value": 2},
            {"date__trunc__day": "2020-11-02", "value": 1},
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
            "aggregations": {
                "value": {
                    "type": "count",
                    "index_by_group": "group1",
                }
            },
            "group_by": "group1,group2",
            "order_by": "-group1__value,-group2",
        },
        [],
        {"search": "4"},
    ),
    # LIMIT NUMBER OF RETURNED GROUPS WITH OFFSET
    (
        {
            "aggregations": {
                "value": {
                    "type": "count",
                }
            },
            "group_by": "group1",
            "order_by": "-value",
            "limit": {
                "limit": 1,
                "offset": 1,
            },
        },
        [{"group1": "1", "value": 2}],
    ),
    # LIMIT WITH GROUP BY MULTIPLE FIELDS WITH OFFSET
    (
        {
            "aggregations": {
                "value": {
                    "type": "count",
                    "index_by_group": "group1",
                }
            },
            "group_by": "group1,group2",
            "order_by": "-group1__value,-group2",
            "limit": {
                "limit": 1,
                "offset": 1,
            },
        },
        [
            {"group1": "1", "group2": "2", "value": 1},
            {"group1": "1", "group2": "1", "value": 1},
        ],
    ),
    # LIMIT WITH GROUP BY MULTIPLE FIELDS AND SHOW OTHER WITH OFFSET
    (
        {
            "aggregations": {
                "value": {
                    "type": "count",
                    "index_by_group": "group1",
                }
            },
            "group_by": "group1,group2",
            "order_by": "-group1__value,-group2",
            "limit": {
                "limit": 1,
                "offset": 1,
                "by_group": "group1",
                "by_aggregation": "value",
                "show_other": True,
            },
        },
        [
            {"group1": "1", "group2": "2", "value": 1},
            {"group1": "1", "group2": "1", "value": 1},
            {"group1": "Other", "group2": "1", "value": 1},
        ],
    ),
]
