from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RightsViewSet, RoyaltyRuleViewSet, RoyaltyLedgerViewSet

router = DefaultRouter()
router.register("licenses", RightsViewSet, basename="license")
router.register("royalty-rules", RoyaltyRuleViewSet, basename="royalty-rule")
router.register("royalty-ledger", RoyaltyLedgerViewSet, basename="royalty-ledger")

urlpatterns = [path("", include(router.urls))]
