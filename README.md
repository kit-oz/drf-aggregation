# Django Rest Framework Aggregation


[![codecov badge](https://codecov.io/gh/kit-oz/drf-aggregation/branch/main/graph/badge.svg?token=X1RWDJI9NG)](https://codecov.io/gh/kit-oz/drf-aggregation)


DRF Mixin for getting aggregations

Key features:

- can get multiple aggregations at once
- can calculate percentile and percent (must be enabled separately)
- grouping by multiple fields
- time series (except SQLite)
- limiting the number of displayed records


## Installing

For installing use pip

```bash
    pip install drf-aggregation
```


## Usage

### Register mixin

The simplest variant of usage is to create a ViewSet with the provided mixin

```python
from drf_aggregation import AggregationMixin


class TicketViewSet(AggregationMixin, GenericViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

urlpatterns = [
    path("aggregation/ticket", TicketViewSet.as_view({"post": "aggregation"})),
]
```

After that you can use it

```http request
POST /aggregation/ticket
Content-Type: application/json
{
    "group_by": "service",
    "limit": 5,
    "order_by": "-total_tasks",
    "aggregations": {
        "total_tasks": {
            "type": "count"
        },
        "average_execution_time": {
            "type": "average",
            "field": "execution_time",
        }
    }
}
```


### Usage in code

Almost all a mixin does is call a function that you can use directly at your way

```python
from drf_aggregation import get_aggregations

result = get_aggregations(
    queryset=Ticket.objects.all(),
    aggregations={
        "total_tasks": {
            "type": "count"
        },
    }
)
```


### Available params

- aggregations - dictionary with aggregations to obtain
    - key - the key under which the aggregation result will be returned
    - value - dictionary with aggregation settings
        - type - aggregation type
        - index_by_group - add an index relative to the specified field for further sorting by it
        - field - required for aggregations: sum, average, minimum, maximum, percentile
        - percentile - from 0 to 1, required for percentile
        - additional_filter - filter parser is used from package [drf-complex-filter](https://github.com/kit-oz/drf-complex-filter), required for percent
- group_by - list of fields to group the result
- order_by - list of fields to sort the result
- limit - number of groups to return or dictionary with settings:
    - limit - number of groups to return
    - offset - shift start of returned groups
    - by_group - which group to limit the result by, by default - the first field for grouping
    - by_aggregation - which aggregation to limit the result by, by default - the first declared aggregation
    - show_other - return the remaining records as one additional group
    - other_label - label of additional group with recordings beyond the limit


### Supported field types

- IntegerField
- FloatField
- DateField (only minimum and maximum)
- DateTimeField (only minimum and maximum)
- DurationField


## Extend aggregation types

By default, only these aggregations are enabled: count, distinct, sum, average, minimum, maximum

Package provide two more aggregations - percent and percentile. But to use them, you need to enable them manually:

```python
# in settings.py
DRF_AGGREGATION_SETTINGS = {
    "AGGREGATION_CLASSES": [
        "drf_aggregation.aggregations.common.CommonAggregations",

        # need to install additional package "drf-complex-filter"
        "drf_aggregation.aggregations.percent.PercentAggregation",

        # works only on PostgreSQL
        "drf_aggregation.aggregations.percentile.PercentileAggregation",
    ],
}
```

You can also create your own aggregations. To do this, create a class with static methods that will be available as an aggregation type

```python
class MyAwesomeAggregations:
    @staticmethod
    def my_aggregation(aggregation: Aggregation, queryset: models.QuerySet):
        name = aggregation.get("name")
        return {f"{name}": models.Count("id")}

# in settings.py
DRF_AGGREGATION_SETTINGS = {
    "AGGREGATION_CLASSES": [
        "drf_aggregation.aggregations.common.CommonAggregations",
        "path.to.MyAwesomeAggregations",
    ],
}

result = get_aggregations(
    queryset=Ticket.objects.all(),
    aggregations={
        "value": {
            "type": "my_aggregation"
        },
    }
)
```


## Usage examples


### Grouping results

To group the result, a comma-separated list of required fields is passed

```python
result = get_aggregations(
    queryset=Ticket.objects.all(),
    aggregations={
        "total_tasks": {
            "type": "count"
        },
    },
    group_by=["field1", "field2"]
)
```


## Sorting the result

When grouping by one field, it is enough to pass a list of fields by which you need to sort the result

```python
result = get_aggregations(
    queryset=Ticket.objects.all(),
    aggregations={
        "total_tasks": {
            "type": "count"
        },
    },
    group_by="field1",
    order_by="field1"
)
```

The requested aggregations can be used as a sorting key

```python
result = get_aggregations(
    queryset=Ticket.objects.all(),
    aggregations={
        "total_tasks": {
            "type": "count"
        },
    },
    group_by="field1",
    order_by="-total_tasks"
)
```

When grouping by multiple fields, you can add an index for the desired group and aggregation pair, after which you can use this index for sorting.

```python
result = get_aggregations(
    queryset=Ticket.objects.all(),
    aggregations={
        "total_tasks": {
            "type": "count",
            "index_by_group": "field1"
        },
    },
    group_by=["field1", "field2"],
    order_by="-field1__total_tasks"
)
```


## Limiting the number of displayed groups

If you have a large number of categories or you need to display only top-N, it is possible to limit the number of returned records

```python
result = get_aggregations(
    queryset=Ticket.objects.all(),
    aggregations={
        "total_tasks": {
            "type": "count",
        },
    },
    group_by="field1",
    order_by="-total_tasks",
    limit=2
)
```

It is also possible to display all other groups as one additional category

```python
result = get_aggregations(
    queryset=Ticket.objects.all(),
    aggregations={
        "total_tasks": {
            "type": "count",
        },
    },
    group_by="field1",
    order_by="-total_tasks",
    limit={
        "limit": 2,
        "show_other": true
    }
)
```

Other parameters to limit:

- by_group - field for selecting the values that will remain, if not passed, the first field for grouping is used
- by_aggregation
- show_other - if true, all groups not included in the top will be displayed as one additional category
- other_label - label for additional category, default "Other"

## Time series

Warning! Doesn't work on SQLite because it doesn't have date / time fields.

To get an aggregation for a time series, you must first annotate your queryset with a truncated date field, and then use that field for grouping.

```python
truncate_rules = { "created_at": "day" }
queryset = truncate_date(Ticket.objects.all(), truncate_rules)

result = get_aggregations(
    queryset=queryset,
    aggregations={
        "total_tasks": {
            "type": "count",
        },
    },
    group_by="created_at__trunc__day",
)
```

If you use AggregationMixin, you just need to pass truncate_rules in the request body.

```http request
POST /aggregation/ticket
Content-Type: application/json
{
    "truncate_rules": { "created_at": "day" },
    "group_by": "created_at__trunc__day",
    "aggregations": {
        "total_tasks": {
            "type": "count"
        },
    }
}
```

Available truncations:

- year
- quarter
- month
- week
- day
- hour
- minute
- second


For mo details about truncations read [Django Docs](https://docs.djangoproject.com/en/3.1/ref/models/database-functions/#trunc)
