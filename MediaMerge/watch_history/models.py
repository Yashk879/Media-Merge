from django.contrib.auth.models import User
from django.db import models
from media_assets.models import MediaAsset

class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch_history")
    asset = models.ForeignKey(MediaAsset, on_delete=models.CASCADE, related_name="watch_events")
    position_seconds = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    watched_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-watched_at"]
        unique_together = ["user", "asset"]
