from rest_framework.viewsets import GenericViewSet
from .mixins import AggregationMixin


class AggregationViewSet(AggregationMixin, GenericViewSet):
    pass
