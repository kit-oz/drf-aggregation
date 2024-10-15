from typing import Dict

from django.db import models


def add_column_indexes(
    queryset: models.QuerySet,
    annotations: Dict[str, models.Aggregate],
    group_indexes: dict,
):
    indexes = {}
    for field_name, aggregation_name in group_indexes.items():
        field_name = field_name.replace(".", "__")
        index_column = f"{field_name}__{aggregation_name}"
        indexes[index_column] = _get_sorting_annotation(
            queryset=queryset,
            annotations=annotations,
            field_name=field_name,
            aggregate_by=aggregation_name,
        )

    if indexes:
        queryset = queryset.annotate(**indexes)

    return queryset


def _get_sorting_annotation(
    queryset: models.QuerySet,
    annotations: Dict[str, models.Aggregate],
    field_name: str,
    aggregate_by: str,
) -> models.Case:
    queryset = queryset.values(field_name)
    queryset = queryset.annotate(**annotations)
    queryset = queryset.order_by(aggregate_by)

    return models.Case(
        *[
            models.When(**{"{}".format(field_name): group[field_name], "then": index})
            for index, group in enumerate(queryset)
        ],
        output_field=models.IntegerField(),
    )
