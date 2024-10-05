from rest_framework.filters import SearchFilter

from .models import TestCaseModel
from .viewsets import AggregationViewSet


class TestCaseViewSet(AggregationViewSet):
    queryset = TestCaseModel.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["group1"]
