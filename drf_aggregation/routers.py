from rest_framework.routers import Route
from rest_framework.routers import SimpleRouter


class AggregationRouter(SimpleRouter):
    """
    A router for read-only APIs, which doesn't use trailing slashes.
    """

    routes = [
        Route(
            url="^{prefix}/aggregation/count$",
            mapping={"get": "count"},
            name="{basename}-aggregation-count",
            detail=False,
            initkwargs={},
        ),
        Route(
            url="^{prefix}/aggregation/sum$",
            mapping={"get": "sum"},
            name="{basename}-aggregation-sum",
            detail=False,
            initkwargs={},
        ),
        Route(
            url="^{prefix}/aggregation/average$",
            mapping={"get": "average"},
            name="{basename}-aggregation-average",
            detail=False,
            initkwargs={},
        ),
        Route(
            url="^{prefix}/aggregation/minimum$",
            mapping={"get": "minimum"},
            name="{basename}-aggregation-minimum",
            detail=False,
            initkwargs={},
        ),
        Route(
            url="^{prefix}/aggregation/maximum$",
            mapping={"get": "maximum"},
            name="{basename}-aggregation-maximum",
            detail=False,
            initkwargs={},
        ),
        Route(
            url="^{prefix}/aggregation/percent$",
            mapping={"get": "percent"},
            name="{basename}-aggregation-percent",
            detail=False,
            initkwargs={},
        ),
        Route(
            url="^{prefix}/aggregation/percentile$",
            mapping={"get": "percentile"},
            name="{basename}-aggregation-percentile",
            detail=False,
            initkwargs={},
        ),
    ]
