from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import MediaAsset, Category
from .serializers import MediaAssetSerializer, CategorySerializer
from .storage import presigned_url
from .tasks import process_asset
from subscriptions.models import Subscription
from rights.models import MediaRight
from django.utils import timezone

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MediaAssetViewSet(viewsets.ModelViewSet):
    serializer_class = MediaAssetSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["media_type", "status", "is_premium"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "view_count", "title"]

    def get_queryset(self):
        return MediaAsset.objects.all().prefetch_related("categories")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def process(self, request, pk=None):
        asset = self.get_object()
        if asset.owner != request.user and not request.user.is_staff:
            return Response({"detail": "Not allowed"}, status=403)
        process_asset.delay(asset.id)
        return Response({"detail": "Media processing queued"})

    @action(detail=True, methods=["get"])
    def stream(self, request, pk=None):
        asset = self.get_object()

        if asset.status != "ready" or not asset.hls_playlist:
            return Response({"detail": "Asset is not ready"}, status=409)

        if asset.is_premium:
            active = Subscription.objects.filter(
                user=request.user, status="active", end_date__gte=timezone.now()
            ).exists()
            if not active:
                return Response({"detail": "Active subscription required"}, status=403)

        has_right = MediaRight.objects.filter(
            asset=asset,
            starts_at__lte=timezone.now(),
            ends_at__gte=timezone.now(),
            is_active=True,
        ).exists()

        if not has_right and not request.user.is_staff:
            return Response({"detail": "Streaming rights are not currently active"}, status=403)

        asset.view_count = asset.view_count + 1
        asset.save(update_fields=["view_count"])

        return Response({
            "playlist": presigned_url(asset.hls_playlist, expires=600),
            "expires_in": 600,
            "protection": "AES-128 HLS / entitlement checked",
        })
