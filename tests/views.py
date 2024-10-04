from rest_framework.filters import SearchFilter

from drf_aggregation.filters import TruncateDateFilter
from drf_aggregation.viewsets import AggregationViewSet

from .models import TestCaseModel


class TestCaseViewSet(AggregationViewSet):
    queryset = TestCaseModel.objects.all()
    filter_backends = [SearchFilter, TruncateDateFilter]
    search_fields = ["group1"]
