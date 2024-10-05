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

Available params:
* aggregations - dict, where key - is 
* group_by - list of fields to group the result
* order_by - list of fields to sort the result
* limit - number of groups to return
* limit_by_group - on which field the limit is set
* limit_by_aggregation - on which aggregation the limit is set
* show_other - if a limit is set, combine other records into an additional group
* other_group_name - title of group "Other"


### Usage in code

Almost all a mixin does is call a function that you can use directly at your way

```python
from drf_aggregation import get_aggregations

queryset = Ticket.objects.all()
aggregations = {
    "total_tasks": {
        "type": "count"
    },
}

result = get_aggregations(queryset, aggregations)
```

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
from drf_aggregation import get_aggregations

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

queryset = Ticket.objects.all()
aggregations = {
    "value": {
        "type": "my_aggregation"
    },
}

result = get_aggregations(queryset, aggregations)
```






In most cases, you want 


### Register aggregations


For enablind



Main 


Create a ViewSet using a ViewSet from a package or by adding a mixin to an existing one



## Aggreagtion

When sending the only parameter "aggregation", a dictionary with the field "value" is returned

```
?aggregation=average

{"value":42.5}
```

Available aggregation types:

- count
- sum
- average
- minimum
- maximum
- percentile
- percent


## Supported field types

- IntegerField
- FloatField
- DateField (only minimum and maximum)
- DateTimeField (only minimum and maximum)
- DurationField


### Additional parameters for different types of aggregations

- field - required for aggregations: sum, average, minimum, maximum, percentile
- percentile - from 0 to 1, required for percentile
- additional_filter - filter parser is used from package [drf-complex-filter](https://github.com/kit-oz/drf-complex-filter), required for percent


## Grouping results

To group the result, a comma-separated list of required fields is passed

```
?aggregation=count&groupBy=field1,field2

[
    {"field1":"value1","field2":"value3","value":2},
    {"field1":"value2","field2":"value3","value":1},
    {"field1":"value2","field2":"value4","value":3}
]
```


## Sorting the result

When grouping by one field, it is enough to pass a list of fields by which you need to sort the result

```
?aggregation=count&groupBy=field1&orderBy=field1

[
    {"field1":"value1","value":2},
    {"field1":"value2","value":1},
    {"field1":"value3","value":3}
]
```

To sort by aggregation result, use "value"

```
?aggregation=count&groupBy=field1&orderBy=-value

[
    {"field1":"value3","value":3},
    {"field1":"value1","value":2},
    {"field1":"value2","value":1}
]
```

To sort when grouping by two or more fields,
you must first add the ColumnIndexFilter filter backend to your ViewSet.

```python
from drf_aggregation.filters import ColumnIndexFilter

class ModelViewSet(AggregationViewSet):
    filter_backends = [ColumnIndexFilter]
```

This filter groups the source queryset by the specified field and preserves the sorting of items.
After that, you can use this index to sort the data grouped in the desired way.

```
?aggregation=count&groupBy=field1,field2&columnIndex=field1&orderBy=-field1__index,-value

[
    {"field1":"value2","field2":"value4","value":3},
    {"field1":"value2","field2":"value3","value":1},
    {"field1":"value1","field2":"value3","value":2}
]
```


## Limiting the number of displayed groups

If you have a large number of categories or you need to display only top-H, it is possible to limit the number of returned records

```
?aggregation=count&groupBy=field1&orderBy=-value&limit=2

[
    {"field1":"value1","value":10},
    {"field1":"value2","value":9}
]
```

It is also possible to display all other groups as one additional category

```
?aggregation=count&groupBy=field1orderBy=-value&&limit=2&showOther=1

[
    {"field1":"value1","value":10},
    {"field1":"value2","value":9},
    {"field1":"Other","value":45}
]
```

Additional options when there is a limit to the number of displayed groups:

- limitBy - field for selecting the values that will remain, if not passed, the first field for grouping is used
- showOther - if "1" is passed, all groups not included in the top will be displayed as one additional category
- otherGroupName - label for additional category, default "Other"

## Time series

Warning! Doesn't work on SQLite because it doesn't have date / time fields.

To display timeseries, you must first add the TruncateDateFilter filter backend to your ViewSet.

```python
from drf_aggregation.filters import TruncateDateFilter

class ModelViewSet(AggregationViewSet):
    filter_backends = [TruncateDateFilter]
```


This filter will allow you to add date fields rounded to the required level,
by which you can group and sort the result

```
?truncateDate=created_at=day&groupBy=created_at__trunc__day

[
    {"created_at__trunc__day": date(2020, 10, 4), "value": 1},
    {"created_at__trunc__day": date(2020, 11, 4), "value": 2},
]
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
