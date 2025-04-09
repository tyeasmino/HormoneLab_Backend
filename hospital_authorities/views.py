from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import HospitalAuthority
from .serializers import HospitalAuthoritySerializer, AllHospitalAuthoritySerializer
from marketing_executives.models import MarketingExecutive
from django.contrib.auth.models import User
from rest_framework import status



class AllHospitalAuthorityViewSet(viewsets.ModelViewSet):
    queryset = HospitalAuthority.objects.all()
    serializer_class = AllHospitalAuthoritySerializer



class HospitalAuthorityViewSet(viewsets.ModelViewSet):
    queryset = HospitalAuthority.objects.all()
    serializer_class = HospitalAuthoritySerializer
    permission_classes = [IsAuthenticated]  

    # Get hospitals under logged-in Marketing Executive
    @action(detail=False, methods=['get'])
    def under_me(self, request):
        user = request.user  
        try:
            marketing_executive = MarketingExecutive.objects.get(user=user)
            location_id = marketing_executive.location  

            hospitals = HospitalAuthority.objects.filter(location_id=location_id)
            serializer = self.get_serializer(hospitals, many=True)
            return Response(serializer.data)

        except MarketingExecutive.DoesNotExist:
            return Response({"error": "User is not linked to any marketing executive"}, status=status.HTTP_400_BAD_REQUEST)

    # **Filter hospitals by location**
    @action(detail=False, methods=['get'])
    def by_location(self, request):
        location_id = request.query_params.get("location_id")

        if not location_id:
            return Response({"error": "location_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        hospitals = HospitalAuthority.objects.filter(location_id=location_id)
        serializer = self.get_serializer(hospitals, many=True)
        return Response(serializer.data)
