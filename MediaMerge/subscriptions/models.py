from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=30)
    max_quality = models.CharField(max_length=20, default="1080p")
    concurrent_streams = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    STATUS = [("active", "Active"), ("cancelled", "Cancelled"), ("expired", "Expired")]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS, default="active")
    provider_reference = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
