from typing import Dict, Union

from django.core.exceptions import ValidationError
from django.db import models

from .settings import aggregation_settings


class Aggregator:
    def __init__(self, queryset: models.QuerySet):
        """Get Aggregator instance

        :param queryset: Django Queryset for aggregation
        """
        self.queryset = queryset.order_by()

    def get_database_aggregation(
        self,
        annotations: Dict[str, models.Aggregate],
        group_by: list = None,
        order_by: list = None,
        limit: int = None,
        limit_by_group: str = None,
        limit_by_aggregation: str = None,
        limit_show_other: bool = False,
        limit_other_label: str = None,
    ) -> Union[dict, list]:
        """Get the aggregation result

        :param annotations: Django aggregation annotation
        :param group_by: list of fields to group the result
        :param order_by: list of fields to sort the result
        :param limit: number of groups to return
        :param limit_by_group: on which field the limit is set
            default is first field for grouping
        :param limit_by_aggregation: on which aggregation the limit is set
            default is first aggregation
        :param limit_show_other: if a limit is set,
            combine other records into an additional group
        :param limit_other_label: title of group "Other"
        :return: list of aggregation results for each set of groups
            in the presence of groupings
            without groupings - a dictionary of the form {value: result}
        """
        if not group_by:
            return self.get_simple_aggregation(annotations)

        queryset = self.queryset.all()
        top_groups_filter = None
        if limit:
            if not limit_by_group:
                limit_by_group = group_by[0]
            if not limit_by_aggregation:
                limit_by_aggregation = list(annotations.keys())[0]
            if not order_by:
                raise ValidationError(
                    {"error": "'order_by' is required when limit is set"}
                )

            top_groups_filter = self._get_top_groups_filter(
                field_name=limit_by_group,
                annotations=annotations,
                order_by=order_by,
                limit=limit,
            )
            queryset = queryset.filter(top_groups_filter)

        if not queryset.exists():
            return []

        queryset = queryset.values(*group_by)
        queryset = queryset.annotate(**annotations)
        if order_by:
            queryset = queryset.order_by(*order_by)

        if not limit or not limit_show_other:
            return list(queryset)

        aggregation_without_top = self.get_aggregation_without_top(
            annotations=annotations,
            group_by=group_by,
            order_by=order_by,
            top_groups_filter=top_groups_filter,
            limit_by_group=limit_by_group,
            limit_by_aggregation=limit_by_aggregation,
        )
        if not aggregation_without_top:
            return list(queryset)

        aggregation = self._merge_aggregations(
            aggregation_1=list(queryset),
            aggregation_2=aggregation_without_top,
            field_name=limit_by_group,
            other_group_name=limit_other_label,
        )

        return list(aggregation)

    def get_simple_aggregation(self, annotations) -> dict:
        """Get aggregation without grouping

        :param annotations: Django aggregation annotation
        :return: Dict {value: result}
        """
        aggregation = (
            self.queryset.annotate(
                _group=models.Value(1, output_field=models.IntegerField())
            )
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
        limit_by_group: str = None,
        limit_by_aggregation: str = None,
    ):
        queryset = self.queryset.exclude(top_groups_filter)
        if queryset.count() == 0:
            return None

        additional_group_by = group_by.copy()
        if limit_by_group in additional_group_by:
            additional_group_by.remove(limit_by_group)

        additional_order_by = order_by.copy()
        limit_index = f"{limit_by_group}__{limit_by_aggregation}"
        if limit_index in additional_order_by:
            additional_order_by.remove(limit_index)
        limit_desc_index = f"-{limit_by_group}__{limit_by_aggregation}"
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
        self, field_name: str, annotations, order_by: list, limit: int
    ) -> models.Q:
        queryset = self.queryset.values(field_name)
        queryset = queryset.annotate(**annotations)
        queryset = queryset.order_by(*order_by)
        top_groups = [group[field_name] for group in queryset[:limit]]

        return models.Q(**{"{}__in".format(field_name): top_groups})

    @staticmethod
    def _merge_aggregations(
        aggregation_1: list,
        aggregation_2: Union[dict, list],
        field_name: str,
        other_group_name: str = None,
    ) -> list:
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
