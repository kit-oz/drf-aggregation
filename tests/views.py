from drf_aggregation.filters import ColumnIndexFilter
from drf_aggregation.filters import TruncateDateFilter
from drf_aggregation.viewsets import AggregationViewSet
from rest_framework.filters import SearchFilter

from .models import TestCaseModel


class TestCaseViewSet(AggregationViewSet):
    queryset = TestCaseModel.objects.all()
    filter_backends = [SearchFilter, TruncateDateFilter, ColumnIndexFilter]
    search_fields = ["group1"]
