=================================
Django Rest Framework Aggregation
=================================

DRF Mixin for getting aggregations

List of possible aggregations:

- count
- sum
- average
- minimum
- maximum
- percentile (work only on PostgreSQL)
- percent

Additional features

- grouping by multiple fields
- grouping by date fields with the required precision (from a second to a year)
- display of top-N records, with the ability to show the rest of the records as a single group

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

    # Total cost of orders
    /order/aggregation?aggregation=sum&aggregationField=price

    # Earliest registration date
    /user/aggregation?aggregation=minimum&aggregationField=date_joined

    # Last travel date
    /trip/aggregation?aggregation=maximum&aggregationField=duration

    # Median salary
    /position/aggregation?aggregation=percentile&aggregationField=salary&percentile=0.5

    # Number of tickets by state
    /ticket/aggregation?aggregation=count&groupByFields=state

    # Top 5 ticket executors
    /ticket/aggregation?aggregation=count&groupByFields=assigned_to&limit=5&limitByField=assigned_to&order=desc

    # Percentage of open tickets by service
    /ticket/aggregation?aggregation=percent&groupByFields=service&additionalFilter={"type":"operator","operator":{"attribute":"state","operator":"=","value":"open"}}

    # Life expectancy depending on the year of birth
    /person/aggregation?aggregation=average&aggregationField=age&annotations={"birth_year":{"field":"birth_date","kind":"year"}}&groupByFields=birth_year

Query parameters
----------------

- aggregation - aggregation type, one of:

    - count
    - sum
    - average
    - minimum
    - maximum
    - percentile
    - percent - return two additional values: "numerator" and "denominator"

- aggregationField - mandatory for aggregations: sum, average, minimum, maximum, percentile
- percentile - from 0 to 1, mandatory for percentile
- outputType - currently only accepts "floats" to properly aggregate integer fields, used for percentile only
- additionalFilter - filter parser is used from package `drf-complex-filter`_, mandatory for percent

The following additional options are available for all aggregation types

- groupBy - comma-separated list of fields, used to group the result by one or more fields, mandatory if limit is set
- annotations - additional annotations for truncating date fields, using `Trunc`_ method from Django, format see examples above
- limit - limits the output to the number of groups of records passed

    - limitByField - field for selecting the values that will remain, mandatory if limit is set
    - order - sorting direction of values: "asc" or "desc"
    - showOther - show groups not included in the top by one category or not
    - otherGroupName - label for a group with records not included in the top

.. _Trunc: https://docs.djangoproject.com/en/3.1/ref/models/database-functions/#trunc
.. _drf-complex-filter: https://github.com/kit-oz/drf-complex-filter

Supported field types
---------------------

Aggregations are available on the following field types:

- IntegerField
- FloatField
- DateField - only minimum and maximum
- DateTimeField - only minimum and maximum
- DurationField
