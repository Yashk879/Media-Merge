from rest_framework import serializers
from .models import WatchHistory

class WatchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchHistory
        fields = "__all__"
        read_only_fields = ["user"]
