from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .helpers import get_aggregation


class AggregationMixin:
    def aggregation(self, request):
        params = request.query_params

        aggregation = params.get("aggregation", None)
        if not aggregation:
            raise ValidationError({"error": "'aggregation' is required"})

        aggregation_field = params["aggregationField"].replace(".", "__") if "aggregationField" in params else None
        limit_by = params["limitBy"].replace(".", "__") if "limitBy" in params else None

        result = get_aggregation(
            queryset=self.filter_queryset(self.get_queryset()),
            aggregation=aggregation,
            aggregation_field=aggregation_field,
            percentile=params.get("percentile", None),
            additional_filter=params.get("additionalFilter", None),
            group_by=self._get_group_by(request),
            order_by=self._get_order_by(request),
            limit=int(params.get("limit", 0)),
            limit_by=limit_by,
            limit_show_other=params.get("showOther", None) == "1",
            limit_other_label=params.get("otherGroupName", None)
        )

        return Response(result)

    @staticmethod
    def _get_group_by(request) -> list:
        group_by = request.query_params.get("groupBy", None)
        group_by = group_by.split(",") if group_by else []

        return [field.replace(".", "__") for field in group_by]

    @staticmethod
    def _get_order_by(request) -> list:
        order_by = request.query_params.get("orderBy", None)
        order_by = order_by.split(",") if order_by else []

        return [field.replace(".", "__") for field in order_by]
