from rest_framework import serializers
from .models import MediaRight, RoyaltyRule, RoyaltyLedger

class MediaRightSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaRight
        fields = "__all__"

class RoyaltyRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoyaltyRule
        fields = "__all__"

class RoyaltyLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoyaltyLedger
        fields = "__all__"
