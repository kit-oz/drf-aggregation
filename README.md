# Django Rest Framework Aggregation

[![codecov badge](https://codecov.io/gh/kit-oz/drf-aggregation/branch/main/graph/badge.svg?token=X1RWDJI9NG)](https://codecov.io/gh/kit-oz/drf-aggregation)
[![PyPI version](https://badge.fury.io/py/drf-aggregation.svg)](https://badge.fury.io/py/drf-aggregation)
[![Python Versions](https://img.shields.io/pypi/pyversions/drf-aggregation.svg)](https://pypi.org/project/drf-aggregation/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Django Rest Framework (DRF) mixin for performing complex data aggregations with ease.

## Key Features

- Perform multiple aggregations simultaneously
- Calculate percentiles and percentages (requires additional setup)
- Group data by multiple fields
- Generate time series data (PostgreSQL, MySQL)
- Flexible result limiting and pagination
- Custom aggregation types support

## Installation

```bash
pip install drf-aggregation
```

## Usage

### With DRF

First, add the `AggregationMixin` to your viewset:

```python
from drf_aggregation import AggregationMixin
from rest_framework.viewsets import GenericViewSet

class TicketViewSet(AggregationMixin, GenericViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
```

Then, register the viewset with your router:

```python
urlpatterns = [
    path("aggregation/ticket", TicketViewSet.as_view({"post": "aggregation"})),
]
```

Once set up, you can make requests like the following:

```http
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
            "field": "execution_time"
        }
    }
}
```

### Direct Usage in Code

You can also use the aggregation function directly:

```python
from drf_aggregation import get_aggregations

result = get_aggregations(
    queryset=Ticket.objects.all(),
    aggregations={
        "total_tasks": {
            "type": "count"
        }
    }
)
```

## Parameters

- **aggregations**: A dictionary specifying the aggregations to perform.
  - **key**: The name under which the aggregation result will be returned.
  - **value**: A dictionary with aggregation settings.
    - **type**: The type of aggregation (e.g., count, sum).
    - **index_by_group**: Index for sorting by a specific field.
    - **field**: Required for sum, average, minimum, maximum, percentile.
    - **percentile**: A value from 0 to 1, required for percentile calculations.
    - **additional_filter**: Uses filter parser from [drf-complex-filter](https://github.com/kit-oz/drf-complex-filter), required for percent.

- **group_by**: List of fields to group the results by.
- **order_by**: List of fields to sort the results.
- **limit**: Number of groups to return or a dictionary with settings:
  - **limit**: Number of groups to return.
  - **offset**: Offset for the start of returned groups.
  - **by_group**: Field to limit the result by, defaults to the first grouping field.
  - **by_aggregation**: Aggregation to limit the result by, defaults to the first declared aggregation.
  - **show_other**: Return remaining records as an additional group.
  - **other_label**: Label for the additional group.

## Supported Field Types

- `IntegerField`
- `FloatField`
- `DateField` (min/max only)
- `DateTimeField` (min/max only)
- `DurationField`

## Extending Aggregation Types

By default, the following aggregations are enabled: `count`, `distinct`, `sum`, `average`, `minimum`, `maximum`.

To enable additional aggregations like percent and percentile, modify your `settings.py`:

```python
# in settings.py
DRF_AGGREGATION_SETTINGS = {
    "AGGREGATION_CLASSES": [
        "drf_aggregation.aggregations.common.CommonAggregations",
        # Requires additional package "drf-complex-filter"
        "drf_aggregation.aggregations.percent.PercentAggregation",
        # Works only on PostgreSQL
        "drf_aggregation.aggregations.percentile.PercentileAggregation",
    ],
}
```

### Custom Aggregations

Create a class with static methods for custom aggregation types:

```python
class MyAggregations:
    @staticmethod
    def my_aggregation(aggregation, queryset):
        name = aggregation.get("name")
        return {f"{name}": models.Count("id")}

# in settings.py
DRF_AGGREGATION_SETTINGS = {
    "AGGREGATION_CLASSES": [
        "drf_aggregation.aggregations.common.CommonAggregations",
        "path.to.MyAggregations",
    ],
}

result = get_aggregations(
    queryset=Ticket.objects.all(),
    aggregations={
        "value": {
            "type": "my_aggregation"
        }
    }
)
```

## Usage Examples

### Grouping Results

Group results by a list of fields:

```python
result = get_aggregations(
    queryset=Ticket.objects.all(),
    aggregations={
        "total_tasks": {
            "type": "count"
        }
    },
    group_by=["field1", "field2"]
)
```

### Sorting Results

Sort results by specified fields:

```python
result = get_aggregations(
    queryset=Ticket.objects.all(),
    aggregations={
        "total_tasks": {
            "type": "count"
        }
    },
    group_by="field1",
    order_by="field1"
)
```

Use aggregations as sorting keys:

```python
result = get_aggregations(
    queryset=Ticket.objects.all(),
    aggregations={
        "total_tasks": {
            "type": "count"
        }
    },
    group_by="field1",
    order_by="-total_tasks"
)
```

### Limiting Displayed Groups

Limit the number of displayed groups:

```python
result = get_aggregations(
    queryset=Ticket.objects.all(),
    aggregations={
        "total_tasks": {
            "type": "count"
        }
    },
    group_by="field1",
    order_by="-total_tasks",
    limit=2
)
```

Display remaining groups as an additional category:

```python
result = get_aggregations(
    queryset=Ticket.objects.all(),
    aggregations={
        "total_tasks": {
            "type": "count"
        }
    },
    group_by="field1",
    order_by="-total_tasks",
    limit={
        "limit": 2,
        "show_other": true
    }
)
```

## Time Series

**Note**: Time series aggregations are not supported on SQLite.

To perform time series aggregations, annotate your queryset with a truncated date field:

```python
truncate_rules = { "created_at": "day" }
queryset = truncate_date(Ticket.objects.all(), truncate_rules)

result = get_aggregations(
    queryset=queryset,
    aggregations={
        "total_tasks": {
            "type": "count"
        }
    },
    group_by="created_at__trunc__day"
)
```

Using `AggregationMixin`, pass `truncate_rules` in the request body:

```http
POST /aggregation/ticket
Content-Type: application/json
{
    "truncate_rules": { "created_at": "day" },
    "group_by": "created_at__trunc__day",
    "aggregations": {
        "total_tasks": {
            "type": "count"
        }
    }
}
```

Available truncation periods: `year`, `quarter`, `month`, `week`, `day`, `hour`, `minute`, `second`

For more details on date truncation, see the [Django documentation](https://docs.djangoproject.com/en/3.1/ref/models/database-functions/#trunc).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
