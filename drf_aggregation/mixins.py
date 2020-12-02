from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .utils import Aggregator
from .helpers import get_annotations


class AggregationMixin:
    def aggregation(self, request):
        aggregation = request.query_params.get("aggregation", None)
        if not aggregation:
            raise ValidationError({"error": "Aggregation is mandatory."})

        queryset = self.filter_queryset(self.get_queryset())

        aggregator = Aggregator(queryset=queryset)
        result = aggregator.get_database_aggregation(
            annotations=get_annotations(aggregation=aggregation,
                                        request=request),
            group_by=self._get_group_by(request=request),
            order_by=self._get_order_by(request=request),
            limit=int(request.query_params.get("limit", 0)),
            limit_by=request.query_params.get("limitBy", None),
            limit_show_other=request.query_params.get("showOther",
                                                      None) == "1",
            limit_other_label=request.query_params.get("otherGroupName", None)
        )

        return Response(result)

    @staticmethod
    def _get_group_by(request) -> list:
        group_by = request.query_params.get("groupBy", None)
        group_by = group_by.split(",") if group_by else []

        return group_by

    @staticmethod
    def _get_order_by(request) -> list:
        group_by = request.query_params.get("orderBy", None)
        group_by = group_by.split(",") if group_by else []

        return group_by
