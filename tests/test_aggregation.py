from rest_framework.test import APITestCase
from parameterized import parameterized
from .models import TestCaseModel
from .fixtures import RECORDS
from .test_data import TEST_DATA


class AggregationTests(APITestCase):
    URL = "/test/aggregation"

    def setUp(self):
        for record in RECORDS:
            record = TestCaseModel(**record)
            record.save()

    @parameterized.expand(TEST_DATA)
    def test_aggregation(self, query, expected_response):
        response = self.client.get(self.URL, query, format="json")
        self.assertEqual(response.status_code, 200,
                         msg=f"Failed on: {query}")
        self.assertEqual(response.data, expected_response,
                         msg=f"Failed on: {query}")
