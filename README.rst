=================================
Django Rest Framework Aggregation
=================================

DRF Mixin for getting aggregations

Key features:

- can calculate percentile (work only on PostgreSQL) and percent
- grouping by multiple fields
- time series
- limiting the number of displayed records

.. attention::

    API not stabilized yet


Installing
----------

For installing use pip

::

    $ pip install drf-aggregation

Usage
-----

Create a ViewSet using a ViewSet from a package or by adding a mixin to an existing one

.. code:: python

    from drf_aggregation.mixins import AggregationMixin
    from drf_aggregation.viewsets import AggregationViewSet


    class MyCustomUserViewSet(AggregationMixin, GenericViewSet):
        queryset = User.objects.all()
        serializer_class = UserSerializer

    class UserViewSet(AggregationViewSet):
        queryset = User.objects.all()
        serializer_class = UserSerializer


Register url

.. code:: python

    from drf_aggregation.routers import AggregationRouter


    aggregation_router = AggregationRouter()
    aggregation_router.register("user", UserViewSet)

    urlpatterns = [
        path("my/custom/endpoint", UserViewSet.as_view({"get": "aggregation"})),
    ]

    urlpatterns += aggregation_router.urls

Get aggregations

::

    # Get the number of users
    /user/aggregation?aggregation=count

    # Last travel date
    /trip/aggregation?aggregation=maximum&aggregationField=duration

    # Median salary
    /position/aggregation?aggregation=percentile&aggregationField=salary&percentile=0.5

    # Top 5 ticket executors
    /ticket/aggregation?aggregation=count&groupBy=assigned_to&limit=5&order=desc

    # Percentage of open tickets by service
    /ticket/aggregation?aggregation=percent&groupBy=service&additionalFilter={"type":"operator","operator":{"attribute":"state","operator":"=","value":"open"}}

    # Life expectancy depending on the year of birth
    /person/aggregation?aggregation=average&aggregationField=age&annotations={"birth_year":{"field":"birth_date","kind":"year"}}&groupBy=birth_year

Supported field types
---------------------

- IntegerField
- FloatField
- DateField (only minimum and maximum)
- DateTimeField (only minimum and maximum)
- DurationField

Aggreagtion
-----------

When sending the only parameter "aggregation", a dictionary with the field "value" is returned

::

    ?aggregation=average
    
    {"value":42.5}

Available aggregation types:

- count
- sum
- average
- minimum
- maximum
- percentile
- percent (return two additional values: "numerator" and "denominator")

Additional parameters for different types of aggregations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- aggregationField - mandatory for aggregations: sum, average, minimum, maximum, percentile
- percentile - from 0 to 1, mandatory for percentile
- outputType - currently only accepts "floats" to properly aggregate integer fields, used for percentile only
- additionalFilter - filter parser is used from package `drf-complex-filter`_, mandatory for percent

.. _drf-complex-filter: https://github.com/kit-oz/drf-complex-filter

Grouping results
----------------

To group the result, a comma-separated list of required fields is passed

::

    ?aggregation=count&groupBy=field1,field2

    [
        {"field1":"value1","field2":"value3","value":2},
        {"field1":"value2","field2":"value3","value":1},
        {"field1":"value2","field2":"value4","value":3}
    ]

Sorting the result
------------------

When grouping by one field, it is enough to pass a list of fields by which you need to sort the result

::

    ?aggregation=count&groupBy=field1&orderBy=field1

    [
        {"field1":"value1","value":2},
        {"field1":"value2","value":1},
        {"field1":"value3","value":3}
    ]

To sort by aggregation result, use "value"

::

    ?aggregation=count&groupBy=field1&orderBy=-value

    [
        {"field1":"value3","value":3},
        {"field1":"value1","value":2},
        {"field1":"value2","value":1}
    ]

To sort when grouping by two or more fields,
you must first add the ColumnIndexFilter filter backend to your ViewSet.

.. code:: python

    from drf_aggregation.filters import ColumnIndexFilter

    class ModelViewSet(AggregationViewSet):
        filter_backends = [ColumnIndexFilter]

This filter groups the source queryset by the specified field and preserves the sorting of items.
After that, you can use this index to sort the data grouped in the desired way.

::

    ?aggregation=count&groupBy=field1,field2&columnIndex=field1&orderBy=-field1__index,-value

    [
        {"field1":"value2","field2":"value4","value":3},
        {"field1":"value2","field2":"value3","value":1},
        {"field1":"value1","field2":"value3","value":2}
    ]


Limiting the number of displayed groups
---------------------------------------

If you have a large number of categories or you need to display only top-H, it is possible to limit the number of returned records

::

    ?aggregation=count&groupBy=field1&orderBy=-value&limit=2

    [
        {"field1":"value1","value":10},
        {"field1":"value2","value":9}
    ]

It is also possible to display all other groups as one additional category

::

    ?aggregation=count&groupBy=field1orderBy=-value&&limit=2&showOther=1
    
    [
        {"field1":"value1","value":10},
        {"field1":"value2","value":9},
        {"field1":"Other","value":45}
    ]

Additional options when there is a limit to the number of displayed groups:

- limitBy - field for selecting the values that will remain, if not passed, the first field for grouping is used
- showOther - if "1" is passed, all groups not included in the top will be displayed as one additional category
- otherGroupName - label for additional category, default "Other"

Time series
-----------

To display timeseries, you must first add the ColumnIndexFilter filter backend to your ViewSet.

.. code:: python

    from drf_aggregation.filters import TruncateDateFilter

    class ModelViewSet(AggregationViewSet):
        filter_backends = [TruncateDateFilter]


This filter will allow you to add date fields rounded to the required level,
by which you can group and sort the result

::

    ?truncateDate=created_at=day&groupBy=created_at__trunc__day

    [
        {"created_at__trunc__day": date(2020, 10, 4), "value": 1},
        {"created_at__trunc__day": date(2020, 11, 4), "value": 2},
    ]

Available truncations:

- year
- quarter
- month
- week
- day
- hour
- minute
- second


For mo details about truncations read `Django Docs`_

.. _Django Docs: https://docs.djangoproject.com/en/3.1/ref/models/database-functions/#trunc
