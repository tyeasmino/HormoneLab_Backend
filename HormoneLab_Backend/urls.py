from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('clients/', include("clients.urls")),
    # path('contactus/', include("contactus.urls")),
    path('hospitals/', include("hospital_authorities.urls")),
    path('executives/', include("marketing_executives.urls")),

    
    path('api-auth/', include("rest_framework.urls")),
    path('auth/', include("dj_rest_auth.urls")),
    path('auth/', include("django.contrib.auth.urls")), 
]
