from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .helpers import get_aggregation


class AggregationMixin:
    def aggregation(self, request):
        aggregation = request.query_params.get("aggregation", None)
        if not aggregation:
            raise ValidationError({"error": "'aggregation' is required"})

        result = get_aggregation(
            queryset=self.filter_queryset(self.get_queryset()),
            aggregation=aggregation,
            aggregation_field=request.query_params.get("aggregationField", None),
            percentile=request.query_params.get("percentile", None),
            output_type=request.query_params.get("outputType", None),
            additional_filter=request.query_params.get("additionalFilter", None),
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
