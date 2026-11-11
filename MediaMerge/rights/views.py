from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import MediaRight, RoyaltyRule, RoyaltyLedger
from .serializers import MediaRightSerializer, RoyaltyRuleSerializer, RoyaltyLedgerSerializer

class RightsViewSet(viewsets.ModelViewSet):
    queryset = MediaRight.objects.all()
    serializer_class = MediaRightSerializer
    permission_classes = [IsAuthenticated]

class RoyaltyRuleViewSet(viewsets.ModelViewSet):
    queryset = RoyaltyRule.objects.all()
    serializer_class = RoyaltyRuleSerializer
    permission_classes = [IsAuthenticated]

class RoyaltyLedgerViewSet(viewsets.ModelViewSet):
    queryset = RoyaltyLedger.objects.all()
    serializer_class = RoyaltyLedgerSerializer
    permission_classes = [IsAuthenticated]
