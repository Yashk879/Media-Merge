from datetime import timedelta
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SubscriptionPlan, Subscription
from .serializers import SubscriptionPlanSerializer, SubscriptionSerializer

class PlanListView(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [AllowAny]

class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            plan = SubscriptionPlan.objects.get(id=request.data["plan_id"])
        except (SubscriptionPlan.DoesNotExist, KeyError):
            return Response({"detail": "Plan not found"}, status=404)

        Subscription.objects.filter(user=request.user, status="active").update(status="cancelled")
        sub = Subscription.objects.create(
            user=request.user,
            plan=plan,
            end_date=timezone.now() + timedelta(days=plan.duration_days),
        )
        return Response(SubscriptionSerializer(sub).data, status=201)

class MySubscriptionView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user).order_by("-end_date")
