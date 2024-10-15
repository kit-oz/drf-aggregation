from typing import Dict, List, Union

from django.core.exceptions import ValidationError
from django.db import models

from .settings import aggregation_settings
from .types import AggregationLimit


class Aggregator:
    def __init__(self, queryset: models.QuerySet):
        """Get Aggregator instance

        :param queryset: Django Queryset for aggregation
        """
        self.queryset = queryset.order_by()

    def get_database_aggregation(
        self,
        annotations: Dict[str, models.Aggregate],
        group_by: List[str] = None,
        order_by: List[str] = None,
        limit: AggregationLimit = None,
    ) -> Union[dict, list]:
        """Get the aggregation result

        :param annotations: Django aggregation annotation
        :param group_by: list of fields to group the result
        :param order_by: list of fields to sort the result
        :param limit: number of groups to return or dictionary with additional limit settings
        :return: list of aggregation results for each set of groups
            in the presence of groupings
            without groupings - a dictionary of the form {value: result}
        """
        if not group_by:
            return self.get_simple_aggregation(annotations)

        if order_by:
            order_by = [field.replace(".", "__") for field in order_by]

        queryset = self.queryset.all()
        top_groups_filter = None

        if limit:
            if not order_by:
                raise ValidationError(
                    {"error": "'order_by' is required when limit is set"}
                )

            (top_groups_filter, other_groups_filter) = self._get_top_groups_filter(
                annotations=annotations, order_by=order_by, limit=limit
            )
            queryset = queryset.filter(top_groups_filter)

        if not queryset.exists():
            return []

        for field in group_by:
            if "." in field:
                queryset = queryset.annotate(
                    **{f"{field}": models.F(field.replace(".", "__"))}
                )
        queryset = queryset.values(*group_by)
        queryset = queryset.annotate(**annotations)
        if order_by:
            queryset = queryset.order_by(*order_by)

        if not limit or not limit.get("show_other", False):
            return list(queryset)

        aggregation_without_top = self.get_aggregation_without_top(
            annotations=annotations,
            group_by=group_by,
            order_by=order_by,
            top_groups_filter=other_groups_filter,
            limit=limit,
        )
        if not aggregation_without_top:
            return list(queryset)

        aggregation = self._merge_aggregations(
            aggregation_1=list(queryset),
            aggregation_2=aggregation_without_top,
            limit=limit,
        )

        return list(aggregation)

    def get_simple_aggregation(self, annotations) -> dict:
        """Get aggregation without grouping

        :param annotations: Django aggregation annotation
        :return: Dict {value: result}
        """
        aggregation = (
            self.queryset.all()
            .annotate(_group=models.Value(1, output_field=models.IntegerField()))
            .values("_group")
            .annotate(**annotations)
            .values(*annotations.keys())
        )
        if aggregation:
            return dict(aggregation[0])

    def get_aggregation_without_top(
        self,
        annotations: Dict[str, models.Aggregate],
        group_by: list,
        order_by: list,
        top_groups_filter: models.Q,
        limit: AggregationLimit = None,
    ):
        queryset = self.queryset.all().exclude(top_groups_filter)
        if queryset.count() == 0:
            return None

        additional_group_by = group_by.copy()
        if limit["by_group"] in additional_group_by:
            additional_group_by.remove(limit["by_group"])

        additional_order_by = order_by.copy()
        limit_index = f"{limit['by_group']}__{limit['by_aggregation']}"
        if limit_index in additional_order_by:
            additional_order_by.remove(limit_index)
        limit_desc_index = f"-{limit['by_group']}__{limit['by_aggregation']}"
        if limit_desc_index in additional_order_by:
            additional_order_by.remove(limit_desc_index)

        aggregator = Aggregator(queryset=queryset)
        aggregation = aggregator.get_database_aggregation(
            annotations=annotations,
            group_by=additional_group_by,
            order_by=additional_order_by,
        )

        return aggregation

    def _get_top_groups_filter(
        self,
        annotations: Dict[str, models.Aggregate],
        order_by: List[str],
        limit: AggregationLimit,
    ) -> models.Q:
        field_name = limit["by_group"].replace(".", "__")
        offset = limit.get("offset", 0)
        if not offset:
            offset = 0
        last_record_index = offset + limit.get("limit", 0)

        queryset = self.queryset.all().values(field_name)
        queryset = queryset.annotate(**annotations)
        queryset = queryset.order_by(order_by[0])
        top_groups_no_offset = [
            group[field_name] for group in queryset[:last_record_index]
        ]
        top_groups = [group for group in top_groups_no_offset[offset:]]

        return (
            models.Q(**{"{}__in".format(field_name): top_groups}),
            models.Q(**{"{}__in".format(field_name): top_groups_no_offset}),
        )

    @staticmethod
    def _merge_aggregations(
        aggregation_1: list,
        aggregation_2: Union[dict, list],
        limit: AggregationLimit,
    ) -> list:
        field_name = limit["by_group"]
        other_group_name = limit["other_label"]
        if not other_group_name:
            other_group_name = aggregation_settings["DEFAULT_OTHER_GROUP_NAME"]

        merged_aggregation = list(aggregation_1)
        if isinstance(aggregation_2, dict):
            aggregation_2[field_name] = other_group_name
            merged_aggregation.append(aggregation_2)
        elif isinstance(aggregation_2, list):
            for result in aggregation_2:
                result[field_name] = other_group_name
                merged_aggregation.append(result)

        return merged_aggregation
