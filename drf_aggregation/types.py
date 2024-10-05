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
