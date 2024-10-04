from typing import Dict

from django.db import models
from django.db.models.functions import Trunc


def truncate_date(queryset: models.QuerySet, truncate_rules: Dict[str, str]):
    annotations = {}
    for field, kind in truncate_rules.items():
        annotations[f"{field}__trunc__{kind}"] = Trunc(field.replace(".", "__"), kind)

    queryset = queryset.annotate(**annotations)

    return queryset
