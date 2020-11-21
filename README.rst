=================================
Django Rest Framework Aggregation
=================================

DRF ViewSet for getting aggregations

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

    GET /user/aggregation?aggregation=count
    GET /order/aggregation?aggregation=sum&aggregationField=price
    GET /user/aggregation?aggregation=minimum&aggregationField=date_joined
    GET /trip/aggregation?aggregation=maximum&aggregationField=duration
    GET /position/aggregation?aggregation=percentile&aggregationField=salary&percentile=0.5
    GET /ticket/aggregation?aggregation=percent&additionalFilter={"type":"operator","operator":{"attribute":"state","operator":"=","value":"open"}}

Possible aggregations
---------------------

Below is a list of possible aggregations and their additional required fields

- count
- sum

    - aggregationField

- average

    - aggregationField

- minimum

    - aggregationField

- maximum

    - aggregationField

- percentile - work only on PostgreSQL

    - aggregationField
    - percentile - from 0 to 1
    - outputType - currently only accepts "floats" for integer aggregation

- percent

    - additionalFilter - filter parser is used from package "drf-complex-filter"

The following additional options are available for all aggregation types

- groupBy - used to group the result by one or more fields, mandatory if limit is set
- limit - limits the output to the number of groups of records passed

    - limitByField - field for selecting the values that will remain, mandatory if limit is set
    - order - sorting direction of values: "asc" or "desc"
    - showOther - show groups not included in the top by one category or not
    - otherGroupName - label for a group with records not included in the top

Supported field types
---------------------

- IntegerField
- FloatField
- DateField - only minimum and maximum
- DateTimeField - only minimum and maximum
- DurationField
