from drf_aggregation.filters import ColumnIndexFilter
from drf_aggregation.filters import TruncateDateFilter
from drf_aggregation.viewsets import AggregationViewSet

from .models import TestCaseModel


class TestCaseViewSet(AggregationViewSet):
    queryset = TestCaseModel.objects.all()
    filter_backends = [TruncateDateFilter, ColumnIndexFilter]
