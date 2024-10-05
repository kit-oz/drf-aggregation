import json
from urllib import parse

from django.db import connection
from parameterized import parameterized
from rest_framework.test import APITestCase

from .fixtures import RECORDS
from .models import TestCaseModel
from .test_data import (
    ANNOTATIONS_TESTING,
    SORTED_GROUPS_TESTING,
    UNSORTED_GROUPS_TESTING,
)


class AggregationTests(APITestCase):
    URL = "/test/aggregation"

    def setUp(self):
        for record in RECORDS:
            record = TestCaseModel(**record)
            record.save()

    @parameterized.expand(ANNOTATIONS_TESTING)
    def test_annotations(self, query, expected_response):
        if connection.vendor != "postgresql":
            types = [
                aggregation["type"] for aggregation in query["aggregations"].values()
            ]
            if "percentile" in types:
                self.skipTest("Percentile only works with PostgreSQL")
        response = self.client.post(self.URL, query, format="json")
        data = json.loads(response.content)
        self.assertEqual(
            response.status_code,
            200,
            msg=f"Failed on: {query}" f"\nResponse: {data}",
        )
        self.assertEqual(
            data,
            expected_response,
            msg=f"Failed on: {query}"
            f"\nResponse: {data}"
            f"\nExpected: {expected_response}",
        )

    @parameterized.expand(UNSORTED_GROUPS_TESTING)
    def test_group_by(self, query, expected_response):
        response = self.client.post(self.URL, query, format="json")
        data = json.loads(response.content)
        self.assertEqual(
            response.status_code,
            200,
            msg=f"Failed on: {query}" f"\nResponse: {data}",
        )
        self.assertEqual(
            len(data),
            len(expected_response),
            msg=f"Failed on: {query}"
            f"\nResponse: {data}"
            f"\nExpected: {expected_response}",
        )
        for result in data:
            self.assertIn(
                result,
                expected_response,
                msg=f"Failed on: {query}"
                f"\nResponse: {data}"
                f"\nExpected: {expected_response}",
            )

    @parameterized.expand(SORTED_GROUPS_TESTING)
    def test_group_by_fields(self, query, expected_response, query_params=None):
        response = self.client.post(
            self.URL,
            query,
            format="json",
            QUERY_STRING=parse.urlencode(query_params) if query_params else None,
        )
        data = json.loads(response.content)
        self.assertEqual(
            response.status_code,
            200,
            msg=f"Failed on: {query}" f"\nResponse: {data}",
        )
        self.assertEqual(
            len(data),
            len(expected_response),
            msg=f"Failed on: {query}"
            f"\nResponse: {data}"
            f"\nExpected: {expected_response}",
        )
        for n in range(len(expected_response)):
            self.assertDictEqual(
                data[n],
                expected_response[n],
                msg=f"Failed on: {query}"
                f"Difference in elements at index: {n}"
                f"\nResponse element: {data[n]}"
                f"\nExpected element: {expected_response[n]}",
            )
