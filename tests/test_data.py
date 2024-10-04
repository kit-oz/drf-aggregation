import json
from datetime import date, datetime, timedelta, timezone

ANNOTATIONS_TESTING = [
    ({"aggregation": "count"}, {"value": 6}),
    ({"aggregation": "sum", "aggregationField": "integer"}, {"value": 15}),
    ({"aggregation": "average", "aggregationField": "integer"}, {"value": 2.5}),
    ({"aggregation": "minimum", "aggregationField": "integer"}, {"value": 0}),
    ({"aggregation": "maximum", "aggregationField": "integer"}, {"value": 5}),
    (
        {"aggregation": "percentile", "aggregationField": "integer", "percentile": 0.5},
        {"value": 2.5},
    ),
    ({"aggregation": "sum", "aggregationField": "float"}, {"value": 15}),
    ({"aggregation": "average", "aggregationField": "float"}, {"value": 2.5}),
    ({"aggregation": "minimum", "aggregationField": "float"}, {"value": 0}),
    ({"aggregation": "maximum", "aggregationField": "float"}, {"value": 5}),
    (
        {"aggregation": "percentile", "aggregationField": "float", "percentile": 0.5},
        {"value": 2.5},
    ),
    (
        {"aggregation": "minimum", "aggregationField": "date"},
        {"value": date(2020, 10, 1)},
    ),
    (
        {"aggregation": "maximum", "aggregationField": "date"},
        {"value": date(2020, 11, 2)},
    ),
    (
        {"aggregation": "minimum", "aggregationField": "datetime"},
        {"value": datetime(2020, 10, 1, 0, 1, tzinfo=timezone.utc)},
    ),
    (
        {"aggregation": "maximum", "aggregationField": "datetime"},
        {"value": datetime(2020, 11, 2, 0, 6, tzinfo=timezone.utc)},
    ),
    (
        {"aggregation": "sum", "aggregationField": "duration"},
        {"value": timedelta(days=21)},
    ),
    (
        {"aggregation": "average", "aggregationField": "duration"},
        {"value": timedelta(days=3, hours=12)},
    ),
    (
        {"aggregation": "minimum", "aggregationField": "duration"},
        {"value": timedelta(days=1)},
    ),
    (
        {"aggregation": "maximum", "aggregationField": "duration"},
        {"value": timedelta(days=6)},
    ),
    (
        {
            "aggregation": "percentile",
            "aggregationField": "duration",
            "percentile": 0.5,
        },
        {"value": timedelta(days=3, hours=12)},
    ),
    (
        {
            "aggregation": "percent",
            "additionalFilter": json.dumps(
                {
                    "type": "operator",
                    "data": {"attribute": "group2", "operator": "=", "value": "1"},
                }
            ),
        },
        {"value_numerator": 3, "value_denominator": 6, "value": 0.5},
    ),
]

UNSORTED_GROUPS_TESTING = [
    # GROUP BY ONE FIELD
    (
        {"aggregation": "count", "group_by": "group1"},
        [
            {"group1": "1", "value": 2},
            {"group1": "2", "value": 1},
            {"group1": "3", "value": 3},
        ],
    ),
    # GROUP BY MULTIPLE FIELDS
    (
        {"aggregation": "count", "group_by": "group1,group2"},
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
            "aggregation": "count",
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
        {"aggregation": "count", "group_by": "group1", "order_by": "-value"},
        [
            {"group1": "3", "value": 3},
            {"group1": "1", "value": 2},
            {"group1": "2", "value": 1},
        ],
    ),
    # ASCENDING SORTING BY VALUE
    (
        {"aggregation": "count", "group_by": "group1", "order_by": "value"},
        [
            {"group1": "2", "value": 1},
            {"group1": "1", "value": 2},
            {"group1": "3", "value": 3},
        ],
    ),
    # SORT BY GROUP NAME
    (
        {"aggregation": "count", "group_by": "group1", "order_by": "group1"},
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
            "aggregation": "count",
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
            "aggregation": "count",
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
            "aggregation": "count",
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
            "aggregation": "count",
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
            "aggregation": "count",
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
            "aggregation": "count",
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
            "aggregation": "count",
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
            "aggregation": "percent",
            "additionalFilter": json.dumps(
                {
                    "type": "operator",
                    "data": {"attribute": "group2", "operator": "=", "value": "2"},
                }
            ),
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
            "aggregation": "count",
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
        {"aggregation": "count", "group_by": "group1"},
        [],
        {"search": "4"},
    ),
    # AGGREGATION ON EMPTY QUERY WITH SORT BY TOTAL GROUP VALUE
    (
        {
            "columnIndex": "group1",
            "aggregation": "count",
            "group_by": "group1,group2",
            "order_by": "-group1__index,-group2",
        },
        [],
        {"search": "4"},
    ),
]
