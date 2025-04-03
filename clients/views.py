from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from rest_framework import viewsets
from . import models, serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User 
from marketing_executives.models import MarketingExecutive




# Create your views here.
class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LocationSerializer

    def get_queryset(self):
        return models.Location.objects.filter(is_selected=False)


class AllLocationViewSet(viewsets.ModelViewSet):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = models.Hospital.objects.all()
    serializer_class = serializers.HospitalSerializer


class ReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Reports.objects.all()
    serializer_class = serializers.ReportsSerializer


    @action(detail=False, methods=['get'])
    def my_reports(self, request):
        user = request.user
        try:
            marketing_executive = MarketingExecutive.objects.get(user=user)
            user_location = marketing_executive.location
        
        except MarketingExecutive.DoesNotExist:
            return Response(
                {"error": "User is not linked to any marketing executive"},
                status=400
            )
    

        reports = self.get_queryset().filter(location = user_location)
        serializer = self.get_serializer(reports, many = True)
        return Response(serializer.data)


