import json

from django.db import models
from drf_complex_filter.utils import generate_query_from_dict
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .aggregates import Percentile
from .utils import get_aggregation


class AggregationViewSet(GenericViewSet):
    def aggregation(self, request):
        annotation = self._get_annotation(request=request)

        result = get_aggregation(
            queryset=self.filter_queryset(self.get_queryset()),
            annotation=annotation,
            group_by=self._get_group_by(request=request),
            order_by=self._get_order(request=request),
            limit=self._get_limit(request=request),
            show_other=self._get_show_other(request=request),
        )

        return Response(result)

    def _get_annotation(self, request):
        aggregation = self._get_aggregation(request)
        if aggregation == 'count':
            return models.Count('id')

        if aggregation == 'sum':
            aggregation_field = self._get_aggregation_field(request=request)
            return models.Sum(aggregation_field)

        if aggregation == 'average':
            aggregation_field = self._get_aggregation_field(request=request)
            return models.Avg(aggregation_field)

        if aggregation == 'minimum':
            aggregation_field = self._get_aggregation_field(request=request)
            return models.Min(aggregation_field)

        if aggregation == 'maximum':
            aggregation_field = self._get_aggregation_field(request=request)
            return models.Max(aggregation_field)

        if aggregation == 'percentile':
            aggregation_field = self._get_aggregation_field(request=request)
            percentile = self._get_percentile(request)
            return Percentile(aggregation_field, percentile)

        if aggregation == 'percent':
            raise NotImplementedError("Grouped percentage not yet implemented")

    @staticmethod
    def _get_aggregation(request) -> str:
        aggregation = request.query_params.get("aggregation", None)
        if not aggregation:
            raise ValidationError({"error": "Aggregation is mandatory."})

        return aggregation

    @staticmethod
    def _get_group_by(request) -> list:
        group_by = request.query_params.get("groupBy", None)
        group_by = group_by.split(",") if group_by else []

        return group_by

    @staticmethod
    def _get_order(request) -> list:
        order = request.query_params.get("order", None)
        if order == "asc":
            return ["value"]
        if order == "desc":
            return ["-value"]

        return []

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
