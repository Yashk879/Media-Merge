from rest_framework import serializers
from .models import MediaAsset, Category, AssetMetadata

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetMetadata
        fields = "__all__"
        read_only_fields = ["asset"]

class MediaAssetSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), write_only=True, source="categories", required=False
    )

    class Meta:
        model = MediaAsset
        fields = [
            "id", "title", "description", "media_type", "original_file",
            "thumbnail", "duration_seconds", "status", "is_premium",
            "tags", "view_count", "created_at", "updated_at",
            "categories", "category_ids",
        ]
        read_only_fields = ["owner", "status", "view_count"]
