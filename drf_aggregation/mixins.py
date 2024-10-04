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

        result = get_aggregations(
            queryset=self.filter_queryset(self.get_queryset()),
            aggregations=aggregations,
            group_by=params.get("group_by", None),
            order_by=params.get("order_by", None),
            limit=int(params.get("limit", 0)),
            limit_by=params.get("limit_by", None),
            limit_show_other=params.get("showOther", False),
            limit_other_label=params.get("otherGroupName", None),
        )

        return Response(result)
