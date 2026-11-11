from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class MediaAsset(models.Model):
    STATUS_CHOICES = [
        ("uploaded", "Uploaded"),
        ("processing", "Processing"),
        ("ready", "Ready"),
        ("failed", "Failed"),
    ]
    MEDIA_TYPES = [("video", "Video"), ("audio", "Audio"), ("image", "Image")]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="media_assets")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES, default="video")
    original_file = models.FileField(upload_to="originals/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    hls_master_key = models.CharField(max_length=500, blank=True)
    hls_playlist = models.CharField(max_length=500, blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="uploaded")
    is_premium = models.BooleanField(default=False)
    tags = models.JSONField(default=list, blank=True)
    view_count = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, blank=True, related_name="assets")

    def __str__(self):
        return self.title

class AssetMetadata(models.Model):
    asset = models.OneToOneField(MediaAsset, on_delete=models.CASCADE, related_name="metadata")
    director = models.CharField(max_length=255, blank=True)
    cast = models.JSONField(default=list, blank=True)
    language = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    release_year = models.PositiveIntegerField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    def __str__(self):
        return f"Metadata: {self.asset.title}"
