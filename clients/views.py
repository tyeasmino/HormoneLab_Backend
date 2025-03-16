from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from rest_framework import viewsets
from . import models, serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.
# class LocationViewSet(viewsets.ModelViewSet):
#     queryset = models.Location.objects.all()
#     serializer_class = serializers.LocationSerializer


class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LocationSerializer

    def get_queryset(self):
        return models.Location.objects.filter(is_selected=False)


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = models.Hospital.objects.all()
    serializer_class = serializers.HospitalSerializer

