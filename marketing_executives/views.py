from django.shortcuts import render
from rest_framework import viewsets
from .models import MarketingExecutive, Deposites, LabServices
from .serializers import MarketingExecutiveSerializer, DepositeSerializer, LabServiceSerializer
from rest_framework.permissions import IsAuthenticated 


# Create your views here.
class LabServiceViewSet(viewsets.ModelViewSet):
    queryset = LabServices.objects.all()
    serializer_class = LabServiceSerializer
 

class AllMarketingExecutiveViewSet(viewsets.ModelViewSet):
    queryset = MarketingExecutive.objects.all()
    serializer_class = MarketingExecutiveSerializer


class MarketingExecutiveViewSet(viewsets.ModelViewSet):
    serializer_class = MarketingExecutiveSerializer

    def get_queryset(self):
        user = self.request.user
        return MarketingExecutive.objects.filter(user=user)


class DepositeViewSet(viewsets.ModelViewSet):
    serializer_class = DepositeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Deposites.objects.filter(user=user)
