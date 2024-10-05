from abc import ABC

from django.core.exceptions import ValidationError
from django.db import models
from drf_complex_filter.utils import ComplexFilter

from ..types import Aggregation


class PercentAggregation:
    @staticmethod
    def percent(aggregation: Aggregation, queryset: models.QuerySet):
        error = {}
        name = aggregation.get("name")

        additional_filter = aggregation.get("additional_filter", None)
        if not additional_filter:
            error["additional_filter"] = "required for aggregation type 'percent'"

        if error:
            raise ValidationError(error, code=422)

        complex_filter = ComplexFilter(model=queryset.model)
        if isinstance(additional_filter, str):
            additional_query, _ = complex_filter.generate_from_string(additional_filter)
        else:
            additional_query, _ = complex_filter.generate_query_from_dict(
                additional_filter
            )
        if not additional_query:
            raise ValidationError(
                {"error": "Additional filter cannot be empty"}, code=422
            )

        return {
            f"{name}_numerator": CountIf(additional_query),
            f"{name}_denominator": models.Count("id"),
            f"{name}": models.ExpressionWrapper(
                models.F(f"{name}_numerator") * 1.0 / models.F(f"{name}_denominator"),
                output_field=models.FloatField(),
            ),
        }


class CountIf(models.Sum, ABC):
    """
    Counts all cases where condition is True
    """

    def __init__(self, condition):
        super().__init__(
            models.Case(
                models.When(condition, then=1),
                default=0,
                output_field=models.IntegerField(),
            )
        )
