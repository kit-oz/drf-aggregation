from typing import Dict, List, TypedDict

from django.db import models
from drf_complex_filter.utils import ComplexFilter
from rest_framework.exceptions import ValidationError

from .aggregates import CountIf, Percentile
from .enums import AggregationType
from .utils import Aggregator

Aggregation = TypedDict(
    "Aggregation",
    {
        "name": str,
        "type": str,
        "field": str,
        "percentile": str,
        "additional_filter": str,
    },
)


def get_aggregations(
    queryset: models.QuerySet,
    aggregations: Dict[str, Aggregation],
    group_by: List[str] | str = None,
    order_by: List[str] | str = None,
    limit: int = 0,
    limit_by: str = None,
    limit_show_other: bool = False,
    limit_other_label: str = None,
):
    if group_by:
        group_by = [
            field.replace(".", "__")
            for field in (
                group_by.split(",") if isinstance(group_by, str) else group_by
            )
        ]

    if order_by:
        order_by = [
            field.replace(".", "__")
            for field in (
                order_by.split(",") if isinstance(order_by, str) else order_by
            )
        ]

    aggregator = Aggregator(queryset=queryset)
    annotations = {}
    for name, aggregation in aggregations.copy().items():
        aggregation["name"] = name
        aggregation["field"] = (
            aggregation["field"].replace(".", "__")
            if "field" in aggregation and aggregation["field"]
            else None
        )
        if not aggregation["type"]:
            raise ValidationError({"error": "'aggregation' is required"})

        annotations = {
            **annotations,
            **get_annotations(queryset=queryset, aggregation=aggregation),
        }

    return aggregator.get_database_aggregation(
        annotations=annotations,
        group_by=group_by,
        order_by=order_by,
        limit=limit,
        limit_by=limit_by.replace(".", "__") if limit_by else None,
        limit_show_other=limit_show_other,
        limit_other_label=limit_other_label,
    )


def get_annotations(
    aggregation: Aggregation,
    queryset: models.QuerySet = None,
) -> dict:
    type = aggregation.get("type")
    name = aggregation.get("name")
    if type == AggregationType.COUNT:
        return {f"{name}": models.Count("id")}

    if type == AggregationType.PERCENT:
        additional_filter = aggregation.get("additional_filter")
        if not additional_filter:
            raise ValidationError(
                {
                    "error": "'additionalFilter' is required for aggregation type 'percent'"
                },
                code=422,
            )

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

    field = aggregation.get("field", None)
    if not field:
        raise ValidationError(
            {"error": f"'aggregationField' is required for aggregation type '{type}'"},
            code=422,
        )

    if type == AggregationType.DISTINCT:
        return {f"{name}": models.Count(field, distinct=True)}

    if type == AggregationType.SUM:
        return {f"{name}": models.Sum(field)}

    if type == AggregationType.AVERAGE:
        return {f"{name}": models.Avg(field)}

    if type == AggregationType.MIN:
        return {f"{name}": models.Min(field)}

    if type == AggregationType.MAX:
        return {f"{name}": models.Max(field)}

    if type == AggregationType.PERCENTILE:
        percentile = aggregation.get("percentile")
        if not percentile:
            raise ValidationError(
                {"error": "'percentile' is required for aggregation type 'percentile'"},
                code=422,
            )

        model: models.Model = queryset.model
        modelField = None
        for field_name in field.split("__"):
            modelField = (
                getattr(modelField, field_name)
                if modelField
                else model._meta.get_field(field_name)
            )

        if modelField.get_internal_type() != "FloatField":
            return {
                f"{name}": Percentile(
                    field, percentile, output_field=models.FloatField()
                )
            }
        return {f"{name}": Percentile(field, percentile)}

    raise ValidationError({"error": f"Unknown aggregation type: {type}"}, code=422)
