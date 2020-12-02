import json
from django.db.models.functions import Trunc
from rest_framework.filters import BaseFilterBackend


class TruncateDateFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user_annotations = self._get_user_annotations(request=request)
        if user_annotations.keys():
            queryset = queryset.annotate(
                **self._get_annotations(user_annotations))

        return queryset

    @staticmethod
    def _get_user_annotations(request) -> dict:
        try:
            user_annotations = json.loads(
                request.query_params.get("annotations", None)
            )
        except (TypeError, json.decoder.JSONDecodeError):
            user_annotations = {}

        return user_annotations

    @staticmethod
    def _get_annotations(user_annotations) -> dict:
        result = {}
        for new_field in user_annotations:
            annotation = user_annotations[new_field]
            result[new_field] = Trunc(annotation["field"], annotation["kind"])

        return result
