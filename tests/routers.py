from rest_framework.routers import Route, SimpleRouter


class AggregationRouter(SimpleRouter):
    """
    A router for read-only APIs, which doesn't use trailing slashes.
    """

    routes = [
        Route(
            url="{prefix}/aggregation",
            mapping={"post": "aggregation"},
            name="{basename}-aggregation",
            detail=False,
            initkwargs={},
        ),
    ]
