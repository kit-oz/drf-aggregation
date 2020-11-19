from drf_aggregation.viewsets import AggregationViewSet

from .models import TestCaseModel


class TestCaseViewSet(AggregationViewSet):
    queryset = TestCaseModel.objects.all()
