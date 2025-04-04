from django.shortcuts import render
from rest_framework import viewsets
from .models import MarketingExecutive, Deposites, LabServices
from .serializers import MarketingExecutiveSerializer, DepositeSerializer, LabServiceSerializer, LocationBasedLabServiceSerializer
from rest_framework.permissions import IsAuthenticated 
from rest_framework.views import APIView
from rest_framework.response import Response
from clients.models import Location

# Create your views here.
class LabServiceViewSet(viewsets.ModelViewSet):
    queryset = LabServices.objects.all()
    serializer_class = LabServiceSerializer
 

class LocationRateLabServicesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            marketing_executive = MarketingExecutive.objects.get(user=user)
            location = marketing_executive.location
            slug = location.slug

            lab_services = LabServices.objects.all()
            serializer = LocationBasedLabServiceSerializer(
                lab_services, many=True, context={'slug': slug}
            )
            return Response(serializer.data)

        except MarketingExecutive.DoesNotExist:
            return Response({"error": "MarketingExecutive not found for this user"}, status=400)
        except Location.DoesNotExist:
            return Response({"error": "Location not found"}, status=400)



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
