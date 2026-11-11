from django.contrib import admin
from .models import MediaAsset, Category, AssetMetadata

admin.site.register(MediaAsset)
admin.site.register(Category)
admin.site.register(AssetMetadata)
