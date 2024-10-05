from django.conf import settings

DEFAULTS = {
    "AGGREGATION_CLASSES": [
        "drf_aggregation.aggregations.common.CommonAggregations",
    ],
    "DEFAULT_OTHER_GROUP_NAME": "Other",
}

DRF_AGGREGATION_SETTINGS = getattr(settings, "DRF_AGGREGATION_SETTINGS", {})

aggregation_settings = {**DEFAULTS, **DRF_AGGREGATION_SETTINGS}
