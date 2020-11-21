from django.db import models


class Aggreagtor:
    OTHER_GROUP_NAME = "Other"

    def __init__(self, queryset: models.QuerySet):
        self.queryset = queryset

    def get_database_aggregation(self,
                                 annotation,
                                 group_by: list = None,
                                 limit: int = None,
                                 limit_field: str = None,
                                 order: str = None,
                                 show_other: bool = False) -> (dict, list):
        pass
        """Get the sum of the values of an aggregation field
    
        :param queryset: Django Queryset for aggregation
        :param annotation: Django aggregation annotation
        :param group_by: list of fields to group the result
        :param limit: number of groups to return
        :param limit_field: on which field the limit is set
        :param order: sort by value to limit groups: 'asc' or 'desc'
        :param show_other: if a limit is set,
            combine other records into an additional group
        :return: list of aggregation results for each set of groups
            in the presence of groupings
            without groupings - a dictionary of the form {value: result}
        """
        if not group_by:
            return dict(self.queryset.aggregate(value=annotation))

        if not limit:
            aggregation = self.queryset.values(*group_by)
            aggregation = aggregation.annotate(value=annotation)
            return list(aggregation)

        top_groups = self._get_top_groups(field_name=limit_field,
                                          annotation=annotation,
                                          limit=limit,
                                          order=order)

        top_groups_filter = None
        for top_group in top_groups:
            query = models.Q(**{"{}".format(limit_field): top_group})
            top_groups_filter = query | top_groups_filter \
                if top_groups_filter else query

        aggregation = self.queryset.filter(top_groups_filter)
        aggregation = aggregation.values(*group_by)
        aggregation = aggregation.annotate(value=annotation)

        if not show_other:
            return list(aggregation)

        additional_queryset = self._get_queryset_without_groups(
            field_name=limit_field,
            values=top_groups)
        if additional_queryset.count() > 0:
            aggregator = Aggreagtor(queryset=additional_queryset)
            additional_aggregation = aggregator.get_database_aggregation(
                annotation=annotation,
                group_by=group_by[1:])
            aggregation = self._merge_aggregations(
                aggregation=aggregation,
                additional_aggregation=additional_aggregation,
                field_name=limit_field,
            )

        return aggregation

    def _get_top_groups(self,
                        field_name: str,
                        annotation,
                        limit: int,
                        order: str = None) -> set:
        queryset = self.queryset.values(field_name)
        queryset = queryset.annotate(value=annotation)
        if order:
            queryset = queryset.order_by(
                'value' if order == 'asc' else '-value')
        top_groups: set = {group[field_name] for group in queryset[: limit]}

        return top_groups

    def _get_queryset_without_groups(self,
                                     field_name: str,
                                     values: set) -> models.QuerySet:
        queryset = self.queryset.all()
        for value in values:
            query = ~models.Q(**{"{}".format(field_name): value})
            queryset = queryset.filter(query)

        return queryset

    def _merge_aggregations(self,
                            aggregation: list,
                            additional_aggregation: (dict, list),
                            field_name: str
                            ) -> list:
        merged_aggregation = list(aggregation)
        if isinstance(additional_aggregation, dict):
            additional_aggregation[field_name] = self.OTHER_GROUP_NAME
            merged_aggregation.append(additional_aggregation)
        elif isinstance(additional_aggregation, list):
            for result in additional_aggregation:
                result[field_name] = self.OTHER_GROUP_NAME
                merged_aggregation.append(result)

        return merged_aggregation
