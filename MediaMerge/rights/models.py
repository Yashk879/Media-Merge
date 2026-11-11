from django.contrib.auth.models import User
from django.db import models
from media_assets.models import MediaAsset

class MediaRight(models.Model):
    asset = models.ForeignKey(MediaAsset, on_delete=models.CASCADE, related_name="rights")
    territory = models.CharField(max_length=100, default="WORLD")
    license_type = models.CharField(max_length=100, default="Streaming")
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    licensor = models.CharField(max_length=255, blank=True)
    exclusivity = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.asset.title} - {self.territory}"

class RoyaltyRule(models.Model):
    asset = models.ForeignKey(MediaAsset, on_delete=models.CASCADE, related_name="royalty_rules")
    recipient = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.asset.title} - {self.recipient}"

class RoyaltyLedger(models.Model):
    asset = models.ForeignKey(MediaAsset, on_delete=models.CASCADE)
    rule = models.ForeignKey(RoyaltyRule, on_delete=models.PROTECT)
    period = models.DateField()
    gross_amount = models.DecimalField(max_digits=12, decimal_places=2)
    royalty_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset.title} - {self.period}"
