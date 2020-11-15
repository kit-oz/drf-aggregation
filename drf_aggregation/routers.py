from rest_framework.routers import Route
from rest_framework.routers import SimpleRouter


class AggregationRouter(SimpleRouter):
    """
    A router for read-only APIs, which doesn't use trailing slashes.
    """

    routes = [
        Route(
            url="{prefix}/aggregation",
            mapping={"get": "aggregation"},
            name="{basename}-aggregation",
            detail=False,
            initkwargs={},
        ),
    ]
