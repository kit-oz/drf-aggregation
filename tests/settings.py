SECRET_KEY = "secret"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "rest_framework",
    "tests",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test",
    }
}

ROOT_URLCONF = "tests.urls"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

USE_TZ = True

DRF_AGGREGATION_SETTINGS = {
    "AGGREGATION_CLASSES": [
        "drf_aggregation.aggregations.common.CommonAggregations",
        "drf_aggregation.aggregations.percent.PercentAggregation",
        "drf_aggregation.aggregations.percentile.PercentileAggregation",
    ],
}
