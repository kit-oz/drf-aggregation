from django.conf import settings

DEFAULTS = {
    "AGGREGATION_CLASSES": [
        "drf_aggregation.aggregations.common.CommonAggregations",
        "drf_aggregation.aggregations.percent.PercentAggregation",
        "drf_aggregation.aggregations.percentile.PercentileAggregation",
    ],
    "DEFAULT_OTHER_GROUP_NAME": "Other",
}

DRF_AGGREGATION_SETTINGS = getattr(settings, "DRF_AGGREGATION_SETTINGS", {})

aggregation_settings = {**DEFAULTS, **DRF_AGGREGATION_SETTINGS}
