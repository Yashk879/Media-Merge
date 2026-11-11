from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MediaAssetViewSet, CategoryViewSet

router = DefaultRouter()
router.register("assets", MediaAssetViewSet, basename="asset")
router.register("categories", CategoryViewSet, basename="category")

urlpatterns = [path("", include(router.urls))]
