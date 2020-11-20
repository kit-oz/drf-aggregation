TEST_DATA = [
    ###########################################################################
    # COUNT
    ###########################################################################
    ({"aggregation": "count"},
     {"value": 6}),

    ({"aggregation": "count", "groupBy": "group", "order": "asc"},
     [{'group': 'group2', 'value': 1}, {'group': 'group1', 'value': 2},
      {'group': 'group3', 'value': 3}]),

    ({"aggregation": "count", "groupBy": "group", "order": "desc"},
     [{'group': 'group3', 'value': 3}, {'group': 'group1', 'value': 2},
      {'group': 'group2', 'value': 1}]),

    ({"aggregation": "count", "groupBy": "group", "order": "desc", "limit": 1},
     [{'group': 'group3', 'value': 3}]),

    ({"aggregation": "count", "groupBy": "group", "order": "desc", "limit": 1,
      "showOther": 1},
     [{'group': 'group3', 'value': 3}, {'group': 'Other', 'value': 3}]),

    ###########################################################################
    # SUM OVER AN INTEGER FIELD
    ###########################################################################
    ({"aggregation": "sum", "aggregationField": "integer"},
     {"value": 15}),

    ({"aggregation": "sum", "aggregationField": "integer", "groupBy": "group",
      "order": "asc"},
     [{'group': 'group2', 'value': 0}, {'group': 'group1', 'value': 3},
      {'group': 'group3', 'value': 12}]),

    ({"aggregation": "sum", "aggregationField": "integer", "groupBy": "group",
      "order": "desc"},
     [{'group': 'group3', 'value': 12}, {'group': 'group1', 'value': 3},
      {'group': 'group2', 'value': 0}]),

    ({"aggregation": "sum", "aggregationField": "integer", "groupBy": "group",
      "order": "desc", "limit": 1},
     [{'group': 'group3', 'value': 12}]),

    ({"aggregation": "sum", "aggregationField": "integer", "groupBy": "group",
      "order": "desc", "limit": 1, "showOther": 1},
     [{'group': 'group3', 'value': 12}, {'group': 'Other', 'value': 3}]),

    ###########################################################################
    # AVERAGE OVER AN INTEGER FIELD
    ###########################################################################
    ({"aggregation": "average", "aggregationField": "integer"},
     {"value": 2.5}),

    ({"aggregation": "average", "aggregationField": "integer",
      "groupBy": "group", "order": "asc"},
     [{'group': 'group2', 'value': 0}, {'group': 'group1', 'value': 1.5},
      {'group': 'group3', 'value': 4}]),

    ({"aggregation": "average", "aggregationField": "integer",
      "groupBy": "group", "order": "desc"},
     [{'group': 'group3', 'value': 4}, {'group': 'group1', 'value': 1.5},
      {'group': 'group2', 'value': 0}]),

    ({"aggregation": "average", "aggregationField": "integer",
      "groupBy": "group", "order": "desc", "limit": 1},
     [{'group': 'group3', 'value': 4}]),

    ({"aggregation": "average", "aggregationField": "integer",
      "groupBy": "group", "order": "desc", "limit": 1, "showOther": 1},
     [{'group': 'group3', 'value': 4}, {'group': 'Other', 'value': 1}]),

    ###########################################################################
    # MINIMUM OVER AN INTEGER FIELD
    ###########################################################################
    ({"aggregation": "minimum", "aggregationField": "integer"},
     {"value": 0}),

    ({"aggregation": "minimum", "aggregationField": "integer",
      "groupBy": "group", "order": "asc"},
     [{'group': 'group2', 'value': 0}, {'group': 'group1', 'value': 1},
      {'group': 'group3', 'value': 3}]),

    ({"aggregation": "minimum", "aggregationField": "integer",
      "groupBy": "group", "order": "desc"},
     [{'group': 'group3', 'value': 3}, {'group': 'group1', 'value': 1},
      {'group': 'group2', 'value': 0}]),

    ({"aggregation": "minimum", "aggregationField": "integer",
      "groupBy": "group", "order": "desc", "limit": 1},
     [{'group': 'group3', 'value': 3}]),

    ({"aggregation": "minimum", "aggregationField": "integer",
      "groupBy": "group", "order": "desc", "limit": 1, "showOther": 1},
     [{'group': 'group3', 'value': 3}, {'group': 'Other', 'value': 0}]),

    ###########################################################################
    # MAXIMUM OVER AN INTEGER FIELD
    ###########################################################################
    ({"aggregation": "maximum", "aggregationField": "integer"},
     {"value": 5}),

    ({"aggregation": "maximum", "aggregationField": "integer",
      "groupBy": "group", "order": "asc"},
     [{'group': 'group2', 'value': 0}, {'group': 'group1', 'value': 2},
      {'group': 'group3', 'value': 5}]),

    ({"aggregation": "maximum", "aggregationField": "integer",
      "groupBy": "group", "order": "desc"},
     [{'group': 'group3', 'value': 5}, {'group': 'group1', 'value': 2},
      {'group': 'group2', 'value': 0}]),

    ({"aggregation": "maximum", "aggregationField": "integer",
      "groupBy": "group", "order": "desc", "limit": 1},
     [{'group': 'group3', 'value': 5}]),

    ({"aggregation": "maximum", "aggregationField": "integer",
      "groupBy": "group", "order": "desc", "limit": 1, "showOther": 1},
     [{'group': 'group3', 'value': 5}, {'group': 'Other', 'value': 2}]),

    ###########################################################################
    # INTEGER PERCENTILE
    ###########################################################################
    ({"aggregation": "percentile", "aggregationField": "integer",
      "percentile": 0.5},
     {"value": 2.5}),

    ({"aggregation": "percentile", "aggregationField": "integer",
      "percentile": 0.5, "groupBy": "group", "order": "asc"},
     [{'group': 'group2', 'value': 0}, {'group': 'group1', 'value': 1.5},
      {'group': 'group3', 'value': 4}]),

    ({"aggregation": "percentile", "aggregationField": "integer",
      "percentile": 0.5, "groupBy": "group", "order": "desc"},
     [{'group': 'group3', 'value': 4}, {'group': 'group1', 'value': 1.5},
      {'group': 'group2', 'value': 0}]),

    ({"aggregation": "percentile", "aggregationField": "integer",
      "percentile": 0.5, "groupBy": "group", "order": "desc", "limit": 1},
     [{'group': 'group3', 'value': 4}]),

    ({"aggregation": "percentile", "aggregationField": "integer",
      "percentile": 0.5, "groupBy": "group", "order": "desc", "limit": 1,
      "showOther": 1},
     [{'group': 'group3', 'value': 4}, {'group': 'Other', 'value': 1}]),
]
