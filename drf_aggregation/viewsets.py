import json

from django.db import models
from drf_complex_filter.utils import generate_query_from_dict
from postgres_stats.aggregates import Percentile
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .utils import get_aggregation


class AggregationViewSet(GenericViewSet):
    @staticmethod
    def _get_group_by(request) -> list:
        group_by = request.query_params.get("groupBy", None)
        group_by = group_by.split(",") if group_by else []

        return group_by

    @staticmethod
    def _get_order_by(request) -> (str, None):
        order = request.query_params.get("orderBy", None)
        if order == "asc":
            return "value"
        if order == "desc":
            return "-value"

    @staticmethod
    def _get_limit(request) -> (int, None):
        limit = request.query_params.get("limit", None)
        return int(limit) if limit else None

    @staticmethod
    def _get_show_other(request) -> bool:
        show_other = request.query_params.get("showOther", None)
        return show_other == "1"

    @staticmethod
    def _get_aggregation_field(request) -> str:
        aggregation_field = request.query_params.get("aggregationField", None)
        if not aggregation_field:
            raise ValidationError({"error": "Aggregation field is mandatory."})

        return aggregation_field

    @staticmethod
    def _get_additional_query(request) -> models.Q:
        try:
            additional_filter = json.loads(
                request.query_params.get("additionalFilter", None)
            )
        except (TypeError, json.decoder.JSONDecodeError):
            raise ValidationError({"error": "Additional filter is mandatory."})
        additional_query = generate_query_from_dict(additional_filter)
        if not additional_query:
            raise ValidationError(
                {"error": "Additional filter cannot be empty."}
            )

        return additional_query

    @staticmethod
    def _get_percentile(request) -> str:
        percentile = request.query_params.get("percentile", None)
        if not percentile:
            raise ValidationError({"error": "Percentile is mandatory."})

        return percentile

    def count(self, request):
        result = get_aggregation(
            queryset=self.filter_queryset(self.get_queryset()),
            annotation=models.Count('id'),
            group_by=self._get_group_by(request=request),
            order_by=self._get_order_by(request=request),
            limit=self._get_limit(request=request),
            show_other=self._get_show_other(request=request),
        )

        return Response(result)

    def sum(self, request):
        aggregation_field = self._get_aggregation_field(request=request)

        result = get_aggregation(
            queryset=self.filter_queryset(self.get_queryset()),
            annotation=models.Sum(aggregation_field),
            group_by=self._get_group_by(request=request),
            order_by=self._get_order_by(request=request),
            limit=self._get_limit(request=request),
            show_other=self._get_show_other(request=request),
        )

        return Response(result)

    def average(self, request):
        aggregation_field = self._get_aggregation_field(request=request)

        result = get_aggregation(
            queryset=self.filter_queryset(self.get_queryset()),
            annotation=models.Avg(aggregation_field),
            group_by=self._get_group_by(request=request),
            order_by=self._get_order_by(request=request),
            limit=self._get_limit(request=request),
            show_other=self._get_show_other(request=request),
        )

        return Response(result)

    def minimum(self, request):
        aggregation_field = self._get_aggregation_field(request=request)

        result = get_aggregation(
            queryset=self.filter_queryset(self.get_queryset()),
            annotation=models.Min(aggregation_field),
            group_by=self._get_group_by(request=request),
            order_by=self._get_order_by(request=request),
            limit=self._get_limit(request=request),
            show_other=self._get_show_other(request=request),
        )

        return Response(result)

    def maximum(self, request):
        aggregation_field = self._get_aggregation_field(request=request)

        result = get_aggregation(
            queryset=self.filter_queryset(self.get_queryset()),
            annotation=models.Max(aggregation_field),
            group_by=self._get_group_by(request=request),
            order_by=self._get_order_by(request=request),
            limit=self._get_limit(request=request),
            show_other=self._get_show_other(request=request),
        )

        return Response(result)

    def percentile(self, request):
        aggregation_field = self._get_aggregation_field(request=request)
        percentile = self._get_percentile(request)

        result = get_aggregation(
            queryset=self.filter_queryset(self.get_queryset()),
            annotation=Percentile(aggregation_field, percentile),
            group_by=self._get_group_by(request=request),
            order_by=self._get_order_by(request=request),
            limit=self._get_limit(request=request),
            show_other=self._get_show_other(request=request),
        )

        return Response(result)

    def percent(self, request):
        additional_query = self._get_additional_query(request)

        raise NotImplementedError("Grouped percentage not yet implemented")
