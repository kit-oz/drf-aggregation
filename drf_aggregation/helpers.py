from typing import Dict, List

from django.core.exceptions import ValidationError
from django.db import models

from .aggregation import Aggregations
from .filters import add_column_indexes
from .types import Aggregation
from .utils import Aggregator


def get_aggregations(
    queryset: models.QuerySet,
    aggregations: Dict[str, Aggregation],
    group_by: List[str] | str = None,
    order_by: List[str] | str = None,
    limit: int = 0,
    limit_by_group: str = None,
    limit_by_aggregation: str = None,
    limit_show_other: bool = False,
    limit_other_label: str = None,
):
    app_aggregations = Aggregations()
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

    annotations = {}
    group_indexes = {}
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
            **app_aggregations.get_annotation(
                aggregation=aggregation, queryset=queryset
            ),
        }

        index_by_group = aggregation.get("index_by_group", None)
        if index_by_group:
            index_by_group = index_by_group.replace(".", "__")
            group_indexes[index_by_group] = aggregation["name"]

    if group_indexes:
        queryset = add_column_indexes(
            queryset, annotations=annotations, group_indexes=group_indexes
        )

    aggregator = Aggregator(queryset=queryset)

    return aggregator.get_database_aggregation(
        annotations=annotations,
        group_by=group_by,
        order_by=order_by,
        limit=limit,
        limit_by_group=limit_by_group.replace(".", "__") if limit_by_group else None,
        limit_by_aggregation=(
            limit_by_aggregation.replace(".", "__") if limit_by_aggregation else None
        ),
        limit_show_other=limit_show_other,
        limit_other_label=limit_other_label,
    )
