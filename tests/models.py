from django.db import models


class TestCaseModel(models.Model):
    number = models.IntegerField()
    date = models.DateField()
    datetime = models.DateTimeField()
    duration = models.DurationField()
