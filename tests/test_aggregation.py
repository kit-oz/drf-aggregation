import json
from rest_framework.test import APITestCase
from parameterized import parameterized
from .models import TestCaseModel
from .fixtures import RECORDS
from .test_data import ANNOTATIONS_TESTING
from .test_data import GROUP_TESTING


class AggregationTests(APITestCase):
    URL = "/test/aggregation"

    def setUp(self):
        for record in RECORDS:
            record = TestCaseModel(**record)
            record.save()

    @parameterized.expand(ANNOTATIONS_TESTING)
    def test_annotations(self, query, expected_response):
        response = self.client.get(self.URL, query, format="json")
        self.assertEqual(response.status_code, 200,
                         msg=f"Failed on: {query}"
                             f"\nResponse: {response.data}"
                             f"\nExpected: {expected_response}")
        self.assertEqual(response.data, expected_response,
                         msg=f"Failed on: {query}"
                             f"\nResponse: {response.data}"
                             f"\nExpected: {expected_response}")

    @parameterized.expand(GROUP_TESTING)
    def test_group_by_fields(self, query, expected_response):
        response = self.client.get(self.URL, query, format="json")
        self.assertEqual(response.status_code, 200,
                         msg=f"Failed on: {query}"
                             f"\nResponse: {response.data}"
                             f"\nExpected: {expected_response}")
        self.assertEqual(len(response.data), len(expected_response),
                         msg=f"Failed on: {query}"
                             f"\nResponse: {response.data}"
                             f"\nExpected: {expected_response}")
        for result in response.data:
            self.assertIn(result, expected_response,
                          msg=f"Failed on: {query}"
                              f"\nResponse: {response.data}"
                              f"\nExpected: {expected_response}")
