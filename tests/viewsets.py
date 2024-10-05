from rest_framework.viewsets import GenericViewSet

from drf_aggregation import AggregationMixin


class AggregationViewSet(AggregationMixin, GenericViewSet):
    pass
