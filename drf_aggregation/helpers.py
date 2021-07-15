from django.db import models
from rest_framework.exceptions import ValidationError
from drf_complex_filter.utils import ComplexFilter

from .aggregates import CountIf
from .aggregates import Percentile
from .enums import Aggregation
from .utils import Aggregator


def get_aggregation(
    queryset: models.QuerySet,
    aggregation: str,
    aggregation_field: str = None,
    percentile: str = None,
    additional_filter: str = None,
    group_by: list = None,
    order_by: list = None,
    limit: int = 0,
    limit_by: str = None,
    limit_show_other: bool = False,
    limit_other_label: str = None,
):
    aggregator = Aggregator(queryset=queryset)
    annotations = get_annotations(
        aggregation=aggregation,
        aggregation_field=aggregation_field,
        percentile=percentile,
        additional_filter=additional_filter,
        queryset=queryset,
    )
    return aggregator.get_database_aggregation(
        annotations=annotations,
        group_by=group_by,
        order_by=order_by,
        limit=limit,
        limit_by=limit_by,
        limit_show_other=limit_show_other,
        limit_other_label=limit_other_label,
    )


def get_annotations(
    aggregation: str,
    aggregation_field: str = None,
    percentile: str = None,
    queryset: models.QuerySet = None,
    additional_filter: str = None,
) -> dict:
    if aggregation == Aggregation.COUNT:
        return {"value": models.Count('id')}

    if aggregation == Aggregation.PERCENT:
        if not additional_filter:
            raise ValidationError({"error": "'additionalFilter' is required for 'aggregation=percent'"}, code=422)

        complex_filter = ComplexFilter()
        additional_query = complex_filter.generate_from_string(additional_filter)
        if not additional_query:
            raise ValidationError({"error": "Additional filter cannot be empty"}, code=422)

        return {
            "numerator": CountIf(additional_query),
            "denominator": models.Count("id"),
            "value": models.ExpressionWrapper(
                models.F("numerator") * 1.0 / models.F("denominator"),
                output_field=models.FloatField())
        }

    if not aggregation_field:
        raise ValidationError({"error": f"'aggregationField' is required for 'aggregation={aggregation}'"}, code=422)

    if aggregation == Aggregation.SUM:
        return {"value": models.Sum(aggregation_field)}

    if aggregation == Aggregation.AVERAGE:
        return {"value": models.Avg(aggregation_field)}

    if aggregation == Aggregation.MIN:
        return {"value": models.Min(aggregation_field)}

    if aggregation == Aggregation.MAX:
        return {"value": models.Max(aggregation_field)}

    if aggregation == Aggregation.PERCENTILE:
        if not percentile:
            raise ValidationError({"error": "'percentile' is required for 'aggregation=percentile'"}, code=422)

        model: models.Model = queryset.model
        field = None
        for field_name in aggregation_field.split("__"):
            field = getattr(field, field_name) if field else model._meta.get_field(field_name)

        if field.get_internal_type() != "FloatField":
            return {"value": Percentile(aggregation_field, percentile,
                                        output_field=models.FloatField())}
        return {"value": Percentile(aggregation_field, percentile)}

    raise ValidationError({"error": "Unknown value for param 'aggregation'"}, code=422)
