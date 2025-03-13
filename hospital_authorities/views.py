from django.shortcuts import render
from rest_framework import viewsets
from .models import HospitalAuthority
from .serializers import HospitalAuthoritySerializer


# Create your views here.
class HospitalAuthorityViewSet(viewsets.ModelViewSet):
    queryset = HospitalAuthority.objects.all()
    serializer_class = HospitalAuthoritySerializer

    