from django.db import models

OTHER_GROUP_NAME = "Other"


def get_aggregation(
        queryset,
        annotation,
        group_by: list = None,
        order_by: list = None,
        limit: int = None,
        show_other: bool = False
) -> (dict, list):
    """Get the sum of the values of an aggregation field

    :param queryset: Django Queryset for aggregation
    :param annotation:
    :param group_by: list of fields to group the result
    :param order_by: list of fields to sort the result
    :param limit: number of record to return
    :param show_other: if a limit is set,
        combine other records into an additional group
    :return: Django Queryset with aggregated data
    """
    if not group_by:
        return queryset.aggregate(value=annotation)

    aggregation = queryset.values(*group_by)
    aggregation = aggregation.annotate(value=annotation)
    if order_by:
        aggregation = aggregation.order_by(*order_by)
    if not limit:
        return list(aggregation)

    aggregation = list(aggregation[: limit])
    if not show_other:
        return aggregation

    main_group_name = group_by[0]
    values = {result[main_group_name] for result in aggregation}
    additional_queryset = _get_queryset_without_groups(
        queryset,
        main_group_name,
        values
    )
    additional_aggregation = get_aggregation(
        queryset=additional_queryset,
        annotation=annotation,
        group_by=group_by[1:]
    )
    aggregation = _merge_aggregations(
        aggregation=aggregation,
        additional_aggregation=additional_aggregation,
        field_name=main_group_name,
    )
    return aggregation


def _get_queryset_without_groups(queryset: models.QuerySet,
                                 field_name: str,
                                 values: set) -> models.QuerySet:
    queryset = queryset.all()
    for value in values:
        query = ~models.Q(**{"{}".format(field_name): value})
        queryset = queryset.filter(query)

    return queryset


def _merge_aggregations(
        aggregation: list,
        additional_aggregation: (dict, list),
        field_name: str
) -> list:
    merged_aggregation = list(aggregation)
    if isinstance(additional_aggregation, dict):
        additional_aggregation[field_name] = OTHER_GROUP_NAME
        merged_aggregation.append(additional_aggregation)
    elif isinstance(additional_aggregation, list):
        for result in additional_aggregation:
            result[field_name] = OTHER_GROUP_NAME
            merged_aggregation.append(result)

    return merged_aggregation
