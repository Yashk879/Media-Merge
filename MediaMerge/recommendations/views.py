from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from media_assets.serializers import MediaAssetSerializer
from .engine import recommend_for_user

class RecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        assets = recommend_for_user(request.user, int(request.query_params.get("limit", 10)))
        return Response(MediaAssetSerializer(assets, many=True).data)
