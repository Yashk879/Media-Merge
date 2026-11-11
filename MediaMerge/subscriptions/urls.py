from django.urls import path
from .views import PlanListView, SubscribeView, MySubscriptionView

urlpatterns = [
    path("plans/", PlanListView.as_view()),
    path("subscribe/", SubscribeView.as_view()),
    path("me/", MySubscriptionView.as_view()),
]
