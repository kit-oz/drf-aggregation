from django.http import JsonResponse

from .filters import truncate_date
from .helpers import get_aggregations


class AggregationMixin:
    def aggregation(self, request):
        params = request.data

        queryset = self.filter_queryset(self.get_queryset())

        truncate_rules = params.get("truncate_rules", None)
        if truncate_rules:
            queryset = truncate_date(queryset, truncate_rules)

        result = get_aggregations(
            queryset=queryset,
            aggregations=params.get("aggregations", None),
            group_by=params.get("group_by", None),
            order_by=params.get("order_by", None),
            limit=int(params.get("limit", 0)),
            limit_by_group=params.get("limit_by_group", None),
            limit_by_aggregation=params.get("limit_by_aggregation", None),
            limit_show_other=params.get("show_other", False),
            limit_other_label=params.get("other_group_name", None),
        )

        return JsonResponse(result, safe=False)
