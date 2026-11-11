from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from media_assets.models import Category
from subscriptions.models import SubscriptionPlan

class Command(BaseCommand):
    help = "Create demo categories and subscription plans"

    def handle(self, *args, **kwargs):
        for name, slug in [
            ("Movies", "movies"),
            ("Series", "series"),
            ("Documentary", "documentary"),
            ("Music", "music"),
            ("Sports", "sports"),
        ]:
            Category.objects.get_or_create(name=name, slug=slug)

        plans = [
            ("Free", 0, 3650, "720p", 1),
            ("Premium", 199, 30, "1080p", 2),
            ("Pro", 399, 30, "4K", 4),
        ]
        for name, price, days, quality, streams in plans:
            SubscriptionPlan.objects.get_or_create(
                name=name,
                defaults={
                    "price": price,
                    "duration_days": days,
                    "max_quality": quality,
                    "concurrent_streams": streams,
                },
            )

        self.stdout.write(self.style.SUCCESS("Demo data created."))
