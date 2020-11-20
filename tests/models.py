from django.db import models


class TestCaseModel(models.Model):
    group = models.CharField(max_length=10)
    integer = models.IntegerField()
    float = models.FloatField()
    date = models.DateField()
    datetime = models.DateTimeField()
    duration = models.DurationField()
