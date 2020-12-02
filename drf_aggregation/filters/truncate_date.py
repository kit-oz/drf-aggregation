from django.db.models.functions import Trunc
from rest_framework.filters import BaseFilterBackend


class TruncateDateFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        truncate_date = request.query_params.get("truncateDate", None)
        if not truncate_date:
            return queryset

        annotations = {}
        for truncate_rule in truncate_date.split(","):
            (field, kind) = truncate_rule.split('=')
            annotations[f'{field}__trunc__{kind}'] = Trunc(field, kind)

        queryset = queryset.annotate(**annotations)

        return queryset
