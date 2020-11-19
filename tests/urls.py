from drf_aggregation.routers import AggregationRouter

from .views import TestCaseViewSet


aggregation_router = AggregationRouter()
aggregation_router.register("test", TestCaseViewSet)

urlpatterns = aggregation_router.urls
