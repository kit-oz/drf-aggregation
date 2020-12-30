from django.db import models
from rest_framework.exceptions import ValidationError


class Aggregator:
    DEFAULT_OTHER_GROUP_NAME = "Other"

    def __init__(self, queryset: models.QuerySet):
        """Get Aggregator instance

        :param queryset: Django Queryset for aggregation
        """
        self.queryset = queryset

    def get_database_aggregation(
            self,
            annotations: dict,
            group_by: list = None,
            order_by: list = None,
            limit: int = None,
            limit_by: str = None,
            limit_show_other: bool = False,
            limit_other_label: str = None
    ) -> (dict, list):
        """Get the aggregation result

        :param annotations: Django aggregation annotation
        :param group_by: list of fields to group the result
        :param order_by: list of fields to sort the result
        :param limit: number of groups to return
        :param limit_by: on which field the limit is set
            default is first field for grouping
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
        if limit and limit > 0:
            if not limit_by:
                limit_by = group_by[0]
            if len(order_by) == 0:
                raise ValidationError(
                    {"error": "If limit is set order_by is needed."}
                )

            top_groups_filter = self._get_top_groups_filter(
                field_name=limit_by,
                annotations=annotations,
                order_by=order_by[0],
                limit=limit)
            queryset = queryset.filter(top_groups_filter)

        if len(queryset) == 0:
            return []

        queryset = queryset.values(*group_by)
        queryset = queryset.annotate(**annotations)
        if order_by and len(order_by) > 0:
            queryset = queryset.order_by(*order_by)

        if not limit or not limit_show_other:
            return list(queryset)

        aggregation_without_top = self.get_aggregation_without_top(
            annotations=annotations,
            group_by=group_by,
            order_by=order_by,
            top_groups_filter=top_groups_filter,
            limit_by=limit_by)
        if not aggregation_without_top:
            return list(queryset)

        aggregation = self._merge_aggregations(
            aggregation=list(queryset),
            additional_aggregation=aggregation_without_top,
            field_name=limit_by,
            other_group_name=limit_other_label)

        return list(aggregation)

    def get_simple_aggregation(self, annotations) -> dict:
        """Get aggregation without grouping

        :param annotations: Django aggregation annotation
        :return: Dict {value: result}
        """
        aggregation = self.queryset.annotate(
            _group=models.Value(1, output_field=models.IntegerField()))
        aggregation = aggregation.values("_group")
        aggregation = aggregation.annotate(**annotations)
        aggregation = aggregation.values(*annotations.keys())
        return dict(aggregation[0])

    def get_aggregation_without_top(
            self,
            annotations: dict,
            group_by: list,
            order_by: list,
            top_groups_filter: models.Q,
            limit_by: str = None,
    ):
        queryset = self.queryset.exclude(top_groups_filter)
        if queryset.count() == 0:
            return None

        additional_group_by = group_by.copy()
        if limit_by in additional_group_by:
            additional_group_by.remove(limit_by)

        aggregator = Aggregator(queryset=queryset)
        aggregation = aggregator.get_database_aggregation(
            annotations=annotations,
            group_by=additional_group_by,
            order_by=order_by)

        return aggregation

    def _get_top_groups_filter(self,
                               field_name: str,
                               annotations,
                               order_by: str,
                               limit: int) -> models.Q:
        queryset = self.queryset.values(field_name)
        queryset = queryset.annotate(**annotations)
        queryset = queryset.order_by(order_by)
        top_groups = [group[field_name] for group in queryset[:limit]]

        return models.Q(**{"{}__in".format(field_name): top_groups})

    def _merge_aggregations(
            self,
            aggregation: list,
            additional_aggregation: (dict, list),
            field_name: str,
            other_group_name: str = None
    ) -> list:
        if not other_group_name:
            other_group_name = self.DEFAULT_OTHER_GROUP_NAME

        merged_aggregation = list(aggregation)
        if isinstance(additional_aggregation, dict):
            additional_aggregation[field_name] = other_group_name
            merged_aggregation.append(additional_aggregation)
        elif isinstance(additional_aggregation, list):
            for result in additional_aggregation:
                result[field_name] = other_group_name
                merged_aggregation.append(result)

        return merged_aggregation
