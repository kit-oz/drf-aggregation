from typing import List

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .helpers import Aggregation, get_aggregations


class AggregationMixin:
    def aggregation(self, request):
        params = request.data

        aggregations: List[Aggregation] = [
            {
                "name": params.get("name", "value"),
                "type": params.get("aggregation", None),
                "aggregation_field": (
                    params["aggregationField"].replace(".", "__")
                    if "aggregationField" in params
                    else None
                ),
                "percentile": params.get("percentile", None),
                "additional_filter": params.get("additionalFilter", None),
            }
        ]
        if not aggregations[0]["type"]:
            raise ValidationError({"error": "'aggregation' is required"})

        limit_by = params["limitBy"].replace(".", "__") if "limitBy" in params else None

        result = get_aggregations(
            queryset=self.filter_queryset(self.get_queryset()),
            aggregations=aggregations,
            group_by=self._get_group_by(params),
            order_by=self._get_order_by(params),
            limit=int(params.get("limit", 0)),
            limit_by=limit_by,
            limit_show_other=params.get("showOther", False),
            limit_other_label=params.get("otherGroupName", None),
        )

        return Response(result)

    @staticmethod
    def _get_group_by(params) -> list:
        group_by = params.get("groupBy", None)
        group_by = group_by.split(",") if group_by else []

        return [field.replace(".", "__") for field in group_by]

    @staticmethod
    def _get_order_by(params) -> list:
        order_by = params.get("orderBy", None)
        order_by = order_by.split(",") if order_by else []

        return [field.replace(".", "__") for field in order_by]
