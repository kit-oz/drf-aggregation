from abc import ABC

from django.db.models import Aggregate, Case, When
from django.db.models.aggregates import Sum
from django.db.models.fields import IntegerField


class Percentile(Aggregate, ABC):
    """From Django Postgres Stats
    https://github.com/rtidatascience/django-postgres-stats

    Accepts a numerical field or expression and a list of fractions and
    returns values for each fraction given corresponding to that fraction in
    that expression.

    If *continuous* is True (the default), the value will be interpolated
    between adjacent values if needed. Otherwise, the value will be the first
    input value whose position in the ordering equals or exceeds the
    specified fraction.

    You will likely have to declare the *output_field* for your results.
    Django cannot guess what type of value will be returned.

    Usage example::

        from django.contrib.postgres.fields import ArrayField

        numbers = [31, 83, 237, 250, 305, 314, 439, 500, 520, 526, 527, 533,
                   540, 612, 831, 854, 857, 904, 928, 973]
        for n in numbers:
            Number.objects.create(n=n)

        results = Number.objects.all().aggregate(
            median=Percentile('n', 0.5, output_field=models.FloatField()))
        assert results['median'] == 526.5

        results = Number.objects.all().aggregate(
            quartiles=Percentile('n', [0.25, 0.5, 0.75],
                                 output_field=ArrayField(models.FloatField())))
        assert results['quartiles'] == [311.75, 526.5, 836.75]

        results = Number.objects.all().aggregate(
            quartiles=Percentile('n', [0.25, 0.5, 0.75],
                                 continuous=False,
                                 output_field=ArrayField(models.FloatField())))
        assert results['quartiles'] == [305, 526, 831]
    """

    function = None
    name = "percentile"
    template = "%(function)s(%(percentiles)s) WITHIN GROUP (ORDER BY %(" \
               "expressions)s)"

    def __init__(self, expression, percentiles, continuous=True, **extra):
        if isinstance(percentiles, (list, tuple)):
            percentiles = "array%(percentiles)s" % {'percentiles': percentiles}
        if continuous:
            extra['function'] = 'PERCENTILE_CONT'
        else:
            extra['function'] = 'PERCENTILE_DISC'

        super().__init__(expression, percentiles=percentiles, **extra)


class CountIf(Sum, ABC):
    """
    Counts all cases where condition is True
    """
    def __init__(self, condition):
        super().__init__(
            Case(
                When(condition, then=1),
                default=0,
                output_field=IntegerField()
            )
        )
