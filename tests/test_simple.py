from datetime import date, datetime, timedelta
from rest_framework.test import APITestCase
from .models import TestCaseModel


class AggregationTests(APITestCase):

    URL = "/test/aggregation"

    def setUp(self):
        record = TestCaseModel(
            number=1,
            date=date.today(),
            datetime=datetime.now(),
            duration=timedelta(days=1),
        )
        record.save()

    def test_simple(self):
        records = TestCaseModel.objects.all()
        self.assertEqual(records.count(), 1)

    def test_request(self):
        query = {
            "aggregation": "count"
        }
        response = self.client.get(self.URL, query, format="json")
        print(response.data)
