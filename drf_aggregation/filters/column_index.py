from django.db import models
from rest_framework import serializers
from rest_framework.filters import BaseFilterBackend

from ..helpers import Aggregation, get_annotations


class ColumnIndexFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        params = request.query_params

        column_index = params.get("columnIndex", None)
        if not column_index:
            return queryset

        aggregation: Aggregation = {
            "name": params.get("name", "value"),
            "type": params.get("aggregation", None),
            "percentile": params.get("percentile", None),
            "additional_filter": params.get("additionalFilter", None),
            "aggregation_field": (
                params["aggregationField"].replace(".", "__")
                if "aggregationField" in params
                else None
            ),
        }

        if not aggregation["type"]:
            raise serializers.ValidationError({"error": "Aggregation is mandatory."})

        annotations = get_annotations(
            aggregation=aggregation,
            queryset=queryset,
        )
        indexes = {}
        for column in column_index.split(","):
            index_column = f"{column}__index"
            indexes[index_column] = self._get_sorting_annotation(
                queryset=queryset, field_name=column, annotations=annotations
            )

        queryset = queryset.annotate(**indexes)

        return queryset

    @staticmethod
    def _get_sorting_annotation(
        queryset: models.QuerySet, field_name: str, annotations: dict
    ) -> models.Case:
        queryset = queryset.values(field_name)
        queryset = queryset.annotate(**annotations)
        queryset = queryset.order_by("value")

        return models.Case(
            *[
                models.When(
                    **{"{}".format(field_name): group[field_name], "then": index}
                )
                for index, group in enumerate(queryset)
            ],
            output_field=models.IntegerField(),
        )
