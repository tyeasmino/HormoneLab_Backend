from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views

router = DefaultRouter()
router.register(r'all_hospital_authorities', views.AllHospitalAuthorityViewSet, basename='all_hospitals')
router.register(r'hospital_authorities', views.HospitalAuthorityViewSet)

urlpatterns = [
    path('', include(router.urls))
]
