from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import HospitalAuthority
from .serializers import HospitalAuthoritySerializer
from marketing_executives.models import MarketingExecutive
from django.contrib.auth.models import User


class HospitalAuthorityViewSet(viewsets.ModelViewSet):
    queryset = HospitalAuthority.objects.all()
    serializer_class = HospitalAuthoritySerializer
    permission_classes = [IsAuthenticated]  # Ensures only logged-in users can access

    # Get hospitals under logged-in user
    @action(detail=False, methods=['get'])
    def under_me(self, request):
        user = request.user  # Get logged-in user
        try:
            marketing_executive = MarketingExecutive.objects.get(user=user)
            location_id = marketing_executive.location  # Get user's location

            hospitals = HospitalAuthority.objects.filter(location_id=location_id)
            serializer = self.get_serializer(hospitals, many=True)
            return Response(serializer.data)

        except MarketingExecutive.DoesNotExist:
            return Response({"error": "User is not linked to any marketing executive"}, status=400)


