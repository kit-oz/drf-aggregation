from django.core.exceptions import ValidationError
from django.db import models

from ..types import Aggregation


class CommonAggregations:
    @staticmethod
    def count(aggregation: Aggregation, queryset: models.QuerySet):
        name = aggregation.get("name")
        return {f"{name}": models.Count("id")}

    @staticmethod
    def distinct(aggregation: Aggregation, queryset: models.QuerySet):
        name = aggregation.get("name")

        field = aggregation.get("field", None)
        if not field:
            raise ValidationError(
                {"field": "required for aggregation type 'distinct'"},
                code=422,
            )

        return {f"{name}": models.Count(field.replace(".", "__"), distinct=True)}

    @staticmethod
    def sum(aggregation: Aggregation, queryset: models.QuerySet):
        name = aggregation.get("name")

        field = aggregation.get("field", None)
        if not field:
            raise ValidationError(
                {"field": "required for aggregation type 'sum'"},
                code=422,
            )

        return {f"{name}": models.Sum(field.replace(".", "__"))}

    @staticmethod
    def average(aggregation: Aggregation, queryset: models.QuerySet):
        name = aggregation.get("name")

        field = aggregation.get("field", None)
        if not field:
            raise ValidationError(
                {"field": "required for aggregation type 'average'"},
                code=422,
            )

        return {f"{name}": models.Avg(field.replace(".", "__"))}

    @staticmethod
    def minimum(aggregation: Aggregation, queryset: models.QuerySet):
        name = aggregation.get("name")

        field = aggregation.get("field", None)
        if not field:
            raise ValidationError(
                {"field": "required for aggregation type 'minimum'"},
                code=422,
            )

        return {f"{name}": models.Min(field.replace(".", "__"))}

    @staticmethod
    def maximum(aggregation: Aggregation, queryset: models.QuerySet):
        name = aggregation.get("name")

        field = aggregation.get("field", None)
        if not field:
            raise ValidationError(
                {"field": "required for aggregation type 'maximum'"},
                code=422,
            )

        return {f"{name}": models.Max(field.replace(".", "__"))}
