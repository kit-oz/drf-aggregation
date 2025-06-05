from typing import TypedDict, Union

Aggregation = TypedDict(
    "Aggregation",
    {
        "name": str,
        "type": str,
        "field": Union[str, None],
        "percentile": Union[str, None],
        "additional_filter": Union[str, None],
        "index_by_group": Union[str, None],
    },
)

AggregationLimit = TypedDict(
    "AggregationLimit",
    {
        "by_group": str,
        "by_aggregation": str,
        "limit": Union[int, None],
        "offset": Union[int, None],
        "show_other": Union[bool, None],
        "other_label": Union[str, None],
    },
)
