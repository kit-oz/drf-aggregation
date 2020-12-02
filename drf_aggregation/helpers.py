import json
from django.db import models
from rest_framework.exceptions import ValidationError
from drf_complex_filter.utils import generate_query_from_dict

from .aggregates import CountIf
from .aggregates import Percentile
from .enums import Aggregation


def get_annotations(aggregation: str, request) -> dict:
    if aggregation == Aggregation.COUNT:
        return {"value": models.Count('id')}

    if aggregation == Aggregation.SUM:
        aggregation_field = get_aggregation_field(request)
        return {"value": models.Sum(aggregation_field)}

    if aggregation == Aggregation.AVERAGE:
        aggregation_field = get_aggregation_field(request)
        return {"value": models.Avg(aggregation_field)}

    if aggregation == Aggregation.MIN:
        aggregation_field = get_aggregation_field(request)
        return {"value": models.Min(aggregation_field)}

    if aggregation == Aggregation.MAX:
        aggregation_field = get_aggregation_field(request)
        return {"value": models.Max(aggregation_field)}

    if aggregation == Aggregation.PERCENTILE:
        aggregation_field = get_aggregation_field(request)
        percentile = get_percentile(request)
        output_type = request.query_params.get("outputType", None)
        if output_type == 'float':
            return {"value": Percentile(aggregation_field, percentile,
                                        output_field=models.FloatField())}
        return {"value": Percentile(aggregation_field, percentile)}

    if aggregation == Aggregation.PERCENT:
        additional_query = get_additional_query(request=request)
        return {
            "numerator": CountIf(additional_query),
            "denominator": models.Count("id"),
            "value": models.ExpressionWrapper(
                models.F("numerator") * 1.0 / models.F("denominator"),
                output_field=models.FloatField())
        }

    raise ValidationError({"error": "Unknown aggregation."})


def get_aggregation_field(request) -> str:
    aggregation_field = request.query_params.get("aggregationField", None)
    if not aggregation_field:
        raise ValidationError({"error": "Aggregation field is mandatory."})

    return aggregation_field


def get_percentile(request) -> str:
    percentile = request.query_params.get("percentile", None)
    if not percentile:
        raise ValidationError({"error": "Percentile is mandatory."})

    return percentile


def get_additional_query(request) -> models.Q:
    try:
        additional_filter = json.loads(
            request.query_params.get("additionalFilter", None)
        )
    except (TypeError, json.decoder.JSONDecodeError):
        raise ValidationError({"error": "Additional filter is mandatory."})
    additional_query = generate_query_from_dict(additional_filter)
    if not additional_query:
        raise ValidationError(
            {"error": "Additional filter cannot be empty."}
        )

    return additional_query
