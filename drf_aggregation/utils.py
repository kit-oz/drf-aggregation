from django.db import models


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
            limit: int = None,
            limit_field: str = None,
            order: str = None,
            show_other: bool = False,
            other_group_name: str = None
    ) -> (dict, list):
        """Get the aggregation result

        :param annotations: Django aggregation annotation
        :param group_by: list of fields to group the result
        :param limit: number of groups to return
        :param limit_field: on which field the limit is set
        :param order: sort by value to limit groups: "asc" or "desc"
        :param show_other: if a limit is set,
            combine other records into an additional group
        :param other_group_name: title of group "Other"
        :return: list of aggregation results for each set of groups
            in the presence of groupings
            without groupings - a dictionary of the form {value: result}
        """
        if not group_by:
            aggregation = self.queryset.annotate(
                _group=models.Value(1, output_field=models.IntegerField()))
            aggregation = aggregation.values("_group")
            aggregation = aggregation.annotate(**annotations)
            aggregation = aggregation.values(*annotations.keys())
            return dict(aggregation[0])

        if not limit:
            aggregation = self.queryset.values(*group_by)
            aggregation = aggregation.annotate(**annotations)
            return list(aggregation)

        top_groups = self._get_top_groups(field_name=limit_field,
                                          annotations=annotations,
                                          limit=limit,
                                          order=order)

        aggregation = self._get_queryset_with_groups(field_name=limit_field,
                                                     values=top_groups)
        aggregation = aggregation.values(*group_by)
        aggregation = aggregation.annotate(**annotations)

        if not show_other:
            return list(aggregation)

        additional_queryset = self._get_queryset_without_groups(
            field_name=limit_field,
            values=top_groups)

        if additional_queryset.count() == 0:
            return list(aggregation)

        additional_group_by = group_by.copy()
        additional_group_by.remove(limit_field)

        aggregator = Aggregator(queryset=additional_queryset)
        additional_aggregation = aggregator.get_database_aggregation(
            annotations=annotations,
            group_by=additional_group_by)
        aggregation = self._merge_aggregations(
            aggregation=aggregation,
            additional_aggregation=additional_aggregation,
            field_name=limit_field,
            other_group_name=other_group_name)

        return list(aggregation)

    def _get_top_groups(self,
                        field_name: str,
                        annotations,
                        limit: int,
                        order: str = None) -> set:
        queryset = self.queryset.values(field_name)
        queryset = queryset.annotate(**annotations)
        if order:
            queryset = queryset.order_by(
                'value' if order == 'asc' else '-value')
        top_groups: set = {group[field_name] for group in queryset[:limit]}

        return top_groups

    def _get_queryset_with_groups(self,
                                  field_name: str,
                                  values: set) -> models.QuerySet:
        top_groups_filter = None
        for value in values:
            query = models.Q(**{"{}".format(field_name): value})
            top_groups_filter = query | top_groups_filter \
                if top_groups_filter else query

        queryset = self.queryset.filter(top_groups_filter)
        return queryset

    def _get_queryset_without_groups(self,
                                     field_name: str,
                                     values: set) -> models.QuerySet:
        queryset = self.queryset.all()
        for value in values:
            query = ~models.Q(**{"{}".format(field_name): value})
            queryset = queryset.filter(query)

        return queryset

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
