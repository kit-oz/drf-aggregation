from datetime import date, datetime, timedelta

TEST_ANNOTATIONS = [
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
     {"value": date(2020, 11, 1)}),

    ({"aggregation": "maximum", "aggregationField": "date"},
     {"value": date(2020, 11, 6)}),

    ({"aggregation": "minimum", "aggregationField": "datetime"},
     {"value": datetime(2020, 11, 1, 0, 1)}),

    ({"aggregation": "maximum", "aggregationField": "datetime"},
     {"value": datetime(2020, 11, 1, 0, 6)}),

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
]
