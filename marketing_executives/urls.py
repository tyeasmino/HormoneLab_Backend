from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views

router = DefaultRouter()
router.register(r'lab-services', views.LabServiceViewSet, basename='lab-services')
router.register(r'marketing-executive', views.MarketingExecutiveViewSet, basename='marketing-executive')
router.register(r'deposites', views.DepositeViewSet, basename='deposites')


urlpatterns = [
    path('', include(router.urls))
]
