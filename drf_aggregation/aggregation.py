from django.core.exceptions import ValidationError
from django.db import models
from django.utils.module_loading import import_string

from .settings import aggregation_settings
from .types import Aggregation


class Aggregations:
    def __init__(self):
        aggregation_classes = []
        for aggregation_path in aggregation_settings["AGGREGATION_CLASSES"]:
            aggregation_classes.append(import_string(aggregation_path))

        class AppAggregations(*aggregation_classes):
            pass

        self.app_aggregations = AppAggregations()

    def get_annotation(
        self,
        aggregation: Aggregation,
        queryset: models.QuerySet,
    ) -> dict:
        aggregation_type = aggregation.get("type")
        if hasattr(self.app_aggregations, aggregation_type) and callable(
            getattr(self.app_aggregations, aggregation_type)
        ):
            get_annotation = getattr(self.app_aggregations, aggregation_type)
            return get_annotation(aggregation=aggregation, queryset=queryset)
        raise ValidationError(
            {"type": f"unknown aggregation type: {aggregation_type}"}, code=422
        )
