from django.db import models
from django.utils.translation import gettext_lazy as _


class Aggregation(models.TextChoices):
    AVERAGE = "average", _("average")
    COUNT = "count", _("count")
    MAX = "maximum", _("maximum")
    MIN = "minimum", _("minimum")
    PERCENT = "percent", _("percent")
    PERCENTILE = "percentile", _("percentile")
    SUM = "sum", _("sum")
