from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter() 
urlpatterns = [ 
    path('register/', views.UserRegistrationApiView.as_view(), name="register"), 
    path('active/<uid64>/<token>/', views.activate, name="active"),
    path('login/', views.UserLoginApiView.as_view(), name="login"), 
    path('logout/', views.UserLogoutApiView.as_view(), name="logout"), 
    path('user_details/', views.user_details, name="user_details"),  
    path('users/', views.all_users_details, name='all_users_details'),
    path('users/<int:user_id>/', views.userid_details, name='userid_details'),
]