from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/media/", include("media_assets.urls")),
    path("api/subscriptions/", include("subscriptions.urls")),
    path("api/rights/", include("rights.urls")),
    path("api/recommendations/", include("recommendations.urls")),
    path("api/watch-history/", include("watch_history.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
]
