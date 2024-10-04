from rest_framework.response import Response

from .helpers import get_aggregations


class AggregationMixin:
    def aggregation(self, request):
        params = request.data

        result = get_aggregations(
            queryset=self.filter_queryset(self.get_queryset()),
            aggregations=params.get("aggregations", None),
            group_by=params.get("group_by", None),
            order_by=params.get("order_by", None),
            limit=int(params.get("limit", 0)),
            limit_by=params.get("limit_by", None),
            limit_show_other=params.get("showOther", False),
            limit_other_label=params.get("otherGroupName", None),
        )

        return Response(result)
