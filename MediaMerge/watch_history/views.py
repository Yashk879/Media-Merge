from rest_framework import viewsets
from .models import WatchHistory
from .serializers import WatchHistorySerializer

class WatchHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = WatchHistorySerializer

    def get_queryset(self):
        return WatchHistory.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        obj, _ = WatchHistory.objects.update_or_create(
            user=self.request.user,
            asset=serializer.validated_data["asset"],
            defaults={
                "position_seconds": serializer.validated_data.get("position_seconds", 0),
                "completed": serializer.validated_data.get("completed", False),
            },
        )
        return obj
