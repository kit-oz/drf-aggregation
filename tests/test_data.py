import json
from datetime import date, datetime, timedelta

ANNOTATIONS_TESTING = [
    ({"aggregation": "count"},
     {"value": 6}),

    ({"aggregation": "sum", "aggregationField": "integer"},
     {"value": 15}),

    ({"aggregation": "average", "aggregationField": "integer"},
     {"value": 2.5}),

    ({"aggregation": "minimum", "aggregationField": "integer"},
     {"value": 0}),

    ({"aggregation": "maximum", "aggregationField": "integer"},
     {"value": 5}),

    ({"aggregation": "percentile", "aggregationField": "integer",
      "percentile": 0.5, "outputType": "float"},
     {"value": 2.5}),

    ({"aggregation": "sum", "aggregationField": "float"},
     {"value": 15}),

    ({"aggregation": "average", "aggregationField": "float"},
     {"value": 2.5}),

    ({"aggregation": "minimum", "aggregationField": "float"},
     {"value": 0}),

    ({"aggregation": "maximum", "aggregationField": "float"},
     {"value": 5}),

    ({"aggregation": "percentile", "aggregationField": "float",
      "percentile": 0.5},
     {"value": 2.5}),

    ({"aggregation": "minimum", "aggregationField": "date"},
     {"value": date(2020, 10, 1)}),

    ({"aggregation": "maximum", "aggregationField": "date"},
     {"value": date(2020, 11, 2)}),

    ({"aggregation": "minimum", "aggregationField": "datetime"},
     {"value": datetime(2020, 10, 1, 0, 1)}),

    ({"aggregation": "maximum", "aggregationField": "datetime"},
     {"value": datetime(2020, 11, 2, 0, 6)}),

    ({"aggregation": "sum", "aggregationField": "duration"},
     {"value": timedelta(days=21)}),

    ({"aggregation": "average", "aggregationField": "duration"},
     {"value": timedelta(days=3, hours=12)}),

    ({"aggregation": "minimum", "aggregationField": "duration"},
     {"value": timedelta(days=1)}),

    ({"aggregation": "maximum", "aggregationField": "duration"},
     {"value": timedelta(days=6)}),

    ({"aggregation": "percentile", "aggregationField": "duration",
      "percentile": 0.5},
     {"value": timedelta(days=3, hours=12)}),

    ({"aggregation": "percent",
      "additionalFilter": json.dumps({"type": "operator",
                                      "data": {"attribute": "group2",
                                               "operator": "=",
                                               "value": "1"}})},
     {"numerator": 3, "denominator": 6, "value": 0.5}),
]

GROUP_TESTING = [
    ({"aggregation": "count", "groupByFields": "group1"},
     [{"group1": "1", "value": 2},
      {"group1": "2", "value": 1},
      {"group1": "3", "value": 3}]),

    ({"aggregation": "count", "groupByFields": "group1,group2"},
     [{"group1": "1", "group2": "1", "value": 1},
      {"group1": "1", "group2": "2", "value": 1},
      {"group1": "2", "group2": "1", "value": 1},
      {"group1": "3", "group2": "1", "value": 1},
      {"group1": "3", "group2": "2", "value": 1},
      {"group1": "3", "group2": "3", "value": 1}]),

    ({"aggregation": "percent",
      "additionalFilter": json.dumps({"type": "operator",
                                      "data": {"attribute": "group2",
                                               "operator": "=",
                                               "value": "2"}}),
      "groupByFields": "group1"},
     [{"group1": "1", "numerator": 1, "denominator": 2, "value": 0.5},
      {"group1": "2", "numerator": 0, "denominator": 1, "value": 0},
      {"group1": "3", "numerator": 1, "denominator": 3, "value": 1 / 3}]),

    ({"aggregation": "count", "groupByFields": "group1",
      "limit": 1, "order": "desc"},
     [{"group1": "3", "value": 3}]),

    ({"aggregation": "count", "groupByFields": "group1",
      "limit": 1, "limitByField": "group1", "order": "asc"},
     [{"group1": "2", "value": 1}]),

    ({"aggregation": "count", "groupByFields": "group1",
      "limit": 1, "order": "desc", "showOther": 1},
     [{"group1": "3", "value": 3},
      {"group1": "Other", "value": 3}]),

    ({"aggregation": "count", "groupByFields": "group1",
      "limit": 3, "order": "desc", "showOther": 1},
     [{"group1": "3", "value": 3},
      {"group1": "1", "value": 2},
      {"group1": "2", "value": 1}]),

    ({"aggregation": "count", "groupByFields": "group1,group2",
      "limit": 1, "order": "desc"},
     [{"group1": "3", "group2": "1", "value": 1},
      {"group1": "3", "group2": "2", "value": 1},
      {"group1": "3", "group2": "3", "value": 1}]),

    ({"aggregation": "count", "groupByFields": "group2,group1",
      "limit": 1, "limitByField": "group1", "order": "desc"},
     [{"group1": "3", "group2": "1", "value": 1},
      {"group1": "3", "group2": "2", "value": 1},
      {"group1": "3", "group2": "3", "value": 1}]),

    ({"aggregation": "percent",
      "additionalFilter": json.dumps({"type": "operator",
                                      "data": {"attribute": "group2",
                                               "operator": "=",
                                               "value": "2"}}),
      "groupByFields": "group1",
      "limit": 1, "order": "desc"},
     [{"group1": "1", "numerator": 1, "denominator": 2, "value": 0.5}]),

    ({"aggregation": "percent",
      "additionalFilter": json.dumps({"type": "operator",
                                      "data": {"attribute": "group2",
                                               "operator": "=",
                                               "value": "2"}}),
      "groupByFields": "group1",
      "limit": 1, "order": "desc", "showOther": 1},
     [{"group1": "1", "numerator": 1, "denominator": 2, "value": 0.5},
      {"group1": "Other", "numerator": 1, "denominator": 4,
       "value": 0.25}]),

    ({"aggregation": "count",
      "annotations": json.dumps({"date_day": {"field": "date",
                                              "kind": "day"}}),
      "groupByFields": "date_day"},
     [{"date_day": date(2020, 10, 1), "value": 2},
      {"date_day": date(2020, 10, 31), "value": 1},
      {"date_day": date(2020, 11, 1), "value": 2},
      {"date_day": date(2020, 11, 2), "value": 1}]),

    ({"aggregation": "count",
      "annotations": json.dumps({"datetime_day": {"field": "datetime",
                                                  "kind": "day"}}),
      "groupByFields": "datetime_day",
      "orderBy": "datetime_day"},
     [{"datetime_day": datetime(2020, 10, 1), "value": 2},
      {"datetime_day": datetime(2020, 10, 31), "value": 1},
      {"datetime_day": datetime(2020, 11, 1), "value": 2},
      {"datetime_day": datetime(2020, 11, 2), "value": 1}]),

    ({"aggregation": "count",
      "annotations": json.dumps({"date_day": {"field": "date", "kind": "day"},
                                 "datetime_day": {"field": "datetime",
                                                  "kind": "day"}}),
      "groupByFields": "date_day,datetime_day",
      "orderBy": "datetime_day"},
     [{"date_day": date(2020, 10, 1),
       "datetime_day": datetime(2020, 11, 2), "value": 1},
      {"date_day": date(2020, 10, 1),
       "datetime_day": datetime(2020, 11, 1), "value": 1},
      {"date_day": date(2020, 10, 31),
       "datetime_day": datetime(2020, 11, 1), "value": 1},
      {"date_day": date(2020, 11, 1),
       "datetime_day": datetime(2020, 10, 31), "value": 1},
      {"date_day": date(2020, 11, 1),
       "datetime_day": datetime(2020, 10, 1), "value": 1},
      {"date_day": date(2020, 11, 2),
       "datetime_day": datetime(2020, 10, 1), "value": 1}]),

    ({"aggregation": "average", "aggregationField": "float",
      "annotations": json.dumps({"date_day": {"field": "date",
                                              "kind": "day"}}),
      "groupByFields": "date_day"},
     [{"date_day": date(2020, 10, 1), "value": 3},
      {"date_day": date(2020, 10, 31), "value": 3},
      {"date_day": date(2020, 11, 1), "value": 3},
      {"date_day": date(2020, 11, 2), "value": 0}]),

    ({"aggregation": "count",
      "annotations": json.dumps({"date_day": {"field": "date",
                                              "kind": "day"}}),
      "groupByFields": "group1,date_day",
      "limit": 1, "order": "desc",
      "showOther": 1},
     [{"group1": "3", "date_day": date(2020, 10, 1), "value": 1},
      {"group1": "3", "date_day": date(2020, 10, 31), "value": 1},
      {"group1": "3", "date_day": date(2020, 11, 1), "value": 1},
      {"group1": "Other", "date_day": date(2020, 10, 1), "value": 1},
      {"group1": "Other", "date_day": date(2020, 11, 1), "value": 1},
      {"group1": "Other", "date_day": date(2020, 11, 2), "value": 1}]),

    ({"aggregation": "count",
      "annotations": json.dumps({"date_day": {"field": "date",
                                              "kind": "day"}}),
      "groupByFields": "date_day,group1",
      "limit": 1, "limitByField": "group1", "order": "desc",
      "showOther": 1},
     [{"group1": "3", "date_day": date(2020, 10, 1), "value": 1},
      {"group1": "3", "date_day": date(2020, 10, 31), "value": 1},
      {"group1": "3", "date_day": date(2020, 11, 1), "value": 1},
      {"group1": "Other", "date_day": date(2020, 10, 1), "value": 1},
      {"group1": "Other", "date_day": date(2020, 11, 1), "value": 1},
      {"group1": "Other", "date_day": date(2020, 11, 2), "value": 1}]),

]
