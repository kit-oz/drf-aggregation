from typing import TypedDict

Aggregation = TypedDict(
    "Aggregation",
    {
        "name": str,
        "type": str,
        "field": str | None,
        "percentile": str | None,
        "additional_filter": str | None,
        "index_by_group": str | None,
    },
)

AggregationLimit = TypedDict(
    "AggregationLimit",
    {
        "by_group": str,
        "by_aggregation": str,
        "limit": int | None,
        "offset": int | None,
        "show_other": bool | None,
        "other_label": str | None,
    },
)
