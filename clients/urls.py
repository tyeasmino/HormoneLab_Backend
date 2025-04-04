from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views

router = DefaultRouter()
router.register(r'all_locations', views.AllLocationViewSet, basename='all_locations')
router.register(r'locations', views.LocationViewSet, basename='locations')
router.register(r'reports', views.ReportViewSet)
router.register(r"user-reports", views.UserReportsViewSet, basename="user-reports") 


urlpatterns = [
    path('', include(router.urls))
]
