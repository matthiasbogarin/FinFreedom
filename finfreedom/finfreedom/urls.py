
from django.contrib import admin
from django.urls import path, include
# from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('finfreedom_frontend.urls')),
    path('finfreedom_api/', include('finfreedom_api.urls')),
]

